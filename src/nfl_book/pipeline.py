"""Build stages: load -> validate -> resolve -> render -> compile -> postbuild.

Everything here is offline. The only network stages are
:func:`prepare_links` and :func:`check_links` (``nfl-book prepare-links [--check]``).
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from nfl_book.config import load_settings
from nfl_book.edition import Loaded, build_media, load, published_edition
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.images import PhotoStats
from nfl_book.models.nfl import Division
from nfl_book.postbuild import Overflow, check_manifest, read_pagemap, write_pagemap
from nfl_book.project import Project
from nfl_book.publishing import booklet_filename
from nfl_book.render import assemble, build_pages, make_env
from nfl_book.render.env import tex
from nfl_book.render.quarto import Quarto, QuartoCli, render_pdf, scan_log
from nfl_book.resolve import resolve
from nfl_book.shortlinks import Shortener, get_shortener
from nfl_book.shortlinks.check import CheckResult, LinkChecker, check_sources
from nfl_book.shortlinks.prepare import PrepareResult, prepare_shortlinks

__all__ = ["BuildResult", "Loaded", "build_media", "load"]


@dataclass
class BuildResult:
    document: Path
    pdf: Path | None = None
    diagnostics: Diagnostics = field(default_factory=Diagnostics)
    overflows: list[Overflow] = field(default_factory=list)
    photos: PhotoStats = field(default_factory=PhotoStats)


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
    diags = Diagnostics()
    build_media(project, model, project.book_build_dir, diags, loaded.settings.book.photos.print)
    if not diags.ok:
        raise ValidationFailed(diags)
    return result


def default_link_checker() -> LinkChecker:
    return LinkChecker()


def check_links(project: Project, checker: LinkChecker | None = None) -> CheckResult:
    """Network stage, read only: report dead and moved source URLs.

    Never shortens a URL, writes ``data/shortlinks.yml``, touches a source file or
    makes QR codes. Invalid content fails before any request is made.
    """
    loaded = load(project, require_shortlinks=False)
    if not loaded.diagnostics.ok:
        raise ValidationFailed(loaded.diagnostics)
    with checker or default_link_checker() as active:
        return check_sources(loaded.content, active)


def build(
    project: Project,
    *,
    pdf: bool = True,
    strict: bool = False,
    division: str | None = None,
    quarto: Quarto | None = None,
) -> BuildResult:
    """Build the book, or one division's booklet, through the shared PDF pipeline."""

    def build_dir(selected: Division | None) -> Path:
        if selected is None:
            return project.book_build_dir
        return project.generated_dir / "booklets" / selected.key / "book"

    edition = published_edition(project, build_dir, division)
    selected = edition.model.division
    directory = build_dir(selected)
    diags = edition.diagnostics
    pages = build_pages(edition.model, edition.media)
    assembled = assemble(
        make_env(project.templates_dir),
        pages,
        directory,
        title=tex(
            f"{edition.settings.book.title}: {selected.name}"
            if selected is not None
            else edition.settings.book.title
        ),
        paper=edition.settings.book.paper,
        styles_dir=project.styles_dir,
        diagnostics=diags,
    )
    result = BuildResult(assembled.document, diagnostics=diags, photos=edition.photos)
    if not pdf:
        return result

    compiled = render_pdf(quarto or QuartoCli(), assembled.document, diags)
    scan_log(assembled.document.with_suffix(".log"), diags)
    pagemap = read_pagemap(compiled)
    pagemap_file = project.pagemap_file if selected is None else directory.parent / "pagemap.json"
    write_pagemap(pagemap, pagemap_file)
    result.overflows = check_manifest(assembled.manifest, pagemap, diags, strict=strict)
    if not diags.ok:
        raise ValidationFailed(diags)
    project.dist_dir.mkdir(parents=True, exist_ok=True)
    result.pdf = project.dist_dir / (
        booklet_filename(selected.key)
        if selected is not None
        else edition.settings.book.output_filename
    )
    shutil.copyfile(compiled, result.pdf)
    return result


def build_booklets(
    project: Project, *, pdf: bool = True, strict: bool = False, quarto: Quarto | None = None
) -> list[BuildResult]:
    """Build every configured division sequentially through the shared PDF pipeline."""
    return [
        build(
            project,
            pdf=pdf,
            strict=strict,
            division=f"{d.conference_id}/{d.id}",
            **({"quarto": quarto} if quarto is not None else {}),
        )
        for d in load_settings(project).league.divisions
    ]


def clean(project: Project) -> list[Path]:
    removed = []
    for directory in (project.generated_dir, project.dist_dir):
        if directory.exists():
            shutil.rmtree(directory)
            removed.append(directory)
    return removed
