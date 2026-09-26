"""Build stages: load -> validate -> resolve -> render -> compile -> postbuild.

Everything here is offline. The only network stage is
:func:`prepare_links` (``nfl-book prepare-links``).
"""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from nfl_book.config import Settings, load_settings
from nfl_book.discovery import discover
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.models.content import Component, Content, Recipe
from nfl_book.postbuild import Overflow, check_manifest, read_pagemap, write_pagemap
from nfl_book.project import Project
from nfl_book.qr import generate_qr_codes
from nfl_book.render import Media, assemble, build_pages, make_env
from nfl_book.render.env import tex
from nfl_book.render.quarto import render_pdf, scan_log
from nfl_book.resolve import BookModel, resolve
from nfl_book.shortlinks import Shortener, ShortlinkCache, get_shortener
from nfl_book.shortlinks.prepare import PrepareResult, prepare_shortlinks
from nfl_book.validation import validate_content


@dataclass
class Loaded:
    settings: Settings
    content: Content
    shortlinks: ShortlinkCache
    diagnostics: Diagnostics


@dataclass
class BuildResult:
    document: Path
    pdf: Path | None = None
    diagnostics: Diagnostics = field(default_factory=Diagnostics)
    overflows: list[Overflow] = field(default_factory=list)


def load(project: Project, *, require_shortlinks: bool = True) -> Loaded:
    """Load settings and content and run all validation (diagnostics are collected)."""
    settings = load_settings(project)
    diags = Diagnostics()
    content = discover(project, settings, diags)
    shortlinks = ShortlinkCache.load(project.shortlinks_file)
    validate_content(
        settings,
        content,
        shortlinks,
        diags,
        indexes_path=project.data_dir / "indexes.yml",
        require_shortlinks=require_shortlinks,
    )
    return Loaded(settings, content, shortlinks, diags)


def filter_paths(diags: Diagnostics, paths: list[Path]) -> Diagnostics:
    """Diagnostics for files at or under any of ``paths``."""
    if not paths:
        return diags
    wanted = [p.resolve() for p in paths]
    return Diagnostics(
        [
            d
            for d in diags
            if d.path is not None
            and any(d.path.resolve() == w or w in d.path.resolve().parents for w in wanted)
        ]
    )


def validate(project: Project, paths: list[Path] | None = None) -> Diagnostics:
    diags = filter_paths(load(project).diagnostics, paths or [])
    if not diags.ok:
        raise ValidationFailed(diags)
    return diags


def prepare_links(project: Project, shortener: Shortener | None = None) -> PrepareResult:
    """Network stage: shorten new source URLs, then (re)generate QR codes."""
    loaded = load(project, require_shortlinks=False)
    if not loaded.diagnostics.ok:
        raise ValidationFailed(loaded.diagnostics)
    result = prepare_shortlinks(
        loaded.content, loaded.shortlinks, shortener or get_shortener("tinyurl")
    )
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    build_media(project, model, project.book_build_dir)
    return result


def _relative(target: Path, start: Path) -> str:
    return Path(os.path.relpath(target, start)).as_posix()


def build_media(project: Project, model: BookModel, build_dir: Path) -> Media:
    """QR codes (from full source URLs) and recipe images, relative to ``build_dir``."""
    sourced: list[tuple[str, Recipe | Component]] = [
        *(("recipe", r) for r in model.recipes_by_id.values()),
        *(("component", c) for c in model.components_by_id.values()),
    ]
    items = [(kind, item.id, item.meta.source.url) for kind, item in sourced if item.meta.source]
    qr = generate_qr_codes(items, project.qr_dir, _relative(project.qr_dir, build_dir))

    images = {}
    assets = project.generated_dir / "assets"
    for recipe in model.recipes_by_id.values():
        if recipe.meta.image:
            source_image = recipe.path.parent / recipe.meta.image
            if source_image.is_file():
                target = assets / f"recipe-{recipe.id}{source_image.suffix.lower()}"
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.is_file() or target.read_bytes() != source_image.read_bytes():
                    shutil.copyfile(source_image, target)
                images[f"recipe:{recipe.id}"] = _relative(target, build_dir)
    return Media(qr=qr, images=images)


def build(project: Project, *, pdf: bool = True, strict: bool = False) -> BuildResult:
    loaded = load(project)
    diags = loaded.diagnostics
    if not diags.ok:
        raise ValidationFailed(diags)
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    build_dir = project.book_build_dir
    media = build_media(project, model, build_dir)
    assembled = assemble(
        make_env(project.templates_dir),
        build_pages(model, media),
        build_dir,
        title=tex(loaded.settings.book.title),
        paper=loaded.settings.book.paper,
        styles_dir=project.styles_dir,
    )
    result = BuildResult(assembled.document, diagnostics=diags)
    if not pdf:
        return result

    compiled = render_pdf(assembled.document)
    scan_log(assembled.document.with_suffix(".log"), diags)
    pagemap = read_pagemap(compiled)
    write_pagemap(pagemap, project.pagemap_file)
    result.overflows = check_manifest(assembled.manifest, pagemap, diags, strict=strict)
    if not diags.ok:
        raise ValidationFailed(diags)
    project.dist_dir.mkdir(parents=True, exist_ok=True)
    result.pdf = project.dist_dir / loaded.settings.book.output_filename
    shutil.copyfile(compiled, result.pdf)
    return result


def clean(project: Project) -> list[Path]:
    removed = []
    for directory in (project.generated_dir, project.dist_dir):
        if directory.exists():
            shutil.rmtree(directory)
            removed.append(directory)
    return removed
