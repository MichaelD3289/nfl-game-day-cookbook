"""The edition every build target renders from: load, validate, resolve, media.

An edition is one versioned build: the settings, the included content, its media and
its version. :func:`published_edition` is the only place the targets get them.
"""

from __future__ import annotations

import os
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from nfl_book.config import Settings, load_settings
from nfl_book.discovery import discover
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.images import PhotoStats, build_photos
from nfl_book.models.common import Status
from nfl_book.models.config import PhotoVariant
from nfl_book.models.content import Component, Content, Recipe
from nfl_book.models.nfl import Division
from nfl_book.project import Project
from nfl_book.publication import is_published
from nfl_book.qr import generate_qr_codes
from nfl_book.references import address, recipe_label
from nfl_book.render.pages import Media
from nfl_book.resolve import BookModel, resolve
from nfl_book.shortlinks import ShortlinkCache
from nfl_book.validation import validate_content


@dataclass
class Loaded:
    settings: Settings
    content: Content
    shortlinks: ShortlinkCache
    diagnostics: Diagnostics


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
        content_root=project.content_root,
        photo_manifest_path=project.data_dir / "photo-manifest.yml",
        require_shortlinks=require_shortlinks,
    )
    return Loaded(settings, content, shortlinks, diags)


def _relative(target: Path, start: Path) -> str:
    return Path(os.path.relpath(target, start)).as_posix()


def build_media(
    project: Project,
    model: BookModel,
    build_dir: Path,
    diagnostics: Diagnostics,
    variant: PhotoVariant,
) -> tuple[Media, PhotoStats]:
    """QR codes and recipe photo variants, relative to ``build_dir``.

    A QR code opens the item's page in this edition of the website. Without
    ``website_url``, and for drafts, it falls back to the full source URL.
    Unreadable photos are reported to ``diagnostics``; source photos are never written.
    """
    all_items: list[tuple[str, Recipe | Component]] = [
        *(("recipe", r) for r in model.recipes_by_id.values()),
        *(("component", c) for c in model.components_by_id.values()),
    ]
    items = [
        (kind, item.id, url)
        for kind, item in all_items
        if (
            url := address(item, edition=model.settings.edition_root).edition_url
            or (item.meta.source and item.meta.source.url)
        )
    ]
    qr = generate_qr_codes(items, project.qr_dir, _relative(project.qr_dir, build_dir))

    sources = {
        recipe_label(recipe.id): recipe.path.parent / recipe.meta.image
        for recipe in model.recipes_by_id.values()
        if recipe.meta.image and (recipe.path.parent / recipe.meta.image).is_file()
    }
    stats = PhotoStats()
    photos = build_photos(sources, variant, project.photo_cache_dir, diagnostics, stats)
    media = Media(
        qr=qr,
        images={key: _relative(p.path, build_dir) for key, p in photos.items()},
        image_sizes={key: p.size for key, p in photos.items()},
    )
    return media, stats


def select_division(settings: Settings, selector: str, project: Project) -> Division:
    """Accept only a configured conference/division pair, before any output writes."""
    selected = next(
        (d for d in settings.league.divisions if selector == f"{d.conference_id}/{d.id}"),
        None,
    )
    if selected is None:
        diags = Diagnostics()
        choices = ", ".join(f"{d.conference_id}/{d.id}" for d in settings.league.divisions)
        diags.error(
            "division",
            f"Unknown division {selector!r}; choose one of: {choices}",
            project.data_dir / "nfl.yml",
        )
        raise ValidationFailed(diags)
    return selected


@dataclass(frozen=True)
class Edition:
    settings: Settings
    model: BookModel
    media: Media
    version: str
    diagnostics: Diagnostics
    photos: PhotoStats


BuildDir = Path | Callable[[Division | None], Path]


def published_edition(
    project: Project,
    build_dir: BuildDir,
    division: str | None = None,
    include: Callable[[Status], bool] = is_published,
    *,
    web: bool = False,
    fresh: bool = False,
) -> Edition:
    """Load, validate and resolve the book, then make its QR codes and photos.

    ``build_dir`` is where the target writes, which media paths are relative to; a
    callable gets the selected division (a booklet's folder depends on it). ``division``
    is ``conference/division``. ``web`` picks the website photo variant, ``fresh`` empties
    ``build_dir`` first. QR codes and photos always live under the root ``generated/``.
    Raises :class:`ValidationFailed` on any error, naming the source file.
    """
    loaded = load(project)
    diags = loaded.diagnostics
    if not diags.ok:
        raise ValidationFailed(diags)
    selected = select_division(loaded.settings, division, project) if division is not None else None
    model = resolve(
        loaded.settings,
        loaded.content,
        loaded.shortlinks.links,
        include=include,
        division=selected,
        content_root=project.content_root,
    )
    directory = build_dir if isinstance(build_dir, Path) else build_dir(selected)
    if fresh and directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)
    book = loaded.settings.book
    media, photos = build_media(
        project, model, directory, diags, book.photos.web if web else book.photos.print
    )
    if not diags.ok:
        raise ValidationFailed(diags)
    return Edition(loaded.settings, model, media, loaded.settings.version, diags, photos)
