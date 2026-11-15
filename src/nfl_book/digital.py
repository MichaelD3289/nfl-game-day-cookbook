"""The resolved book and portable media shared by the digital formats."""

import shutil
from dataclasses import dataclass
from pathlib import Path

from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.images import PhotoStats
from nfl_book.pipeline import build_media, load
from nfl_book.project import Project
from nfl_book.references import component_label, html_id, recipe_label
from nfl_book.render.pages import Media
from nfl_book.resolve import BookModel, resolve


@dataclass(frozen=True)
class Prepared:
    """The published book and its media, ready for a format to build its page views."""

    model: BookModel
    media: Media
    diagnostics: Diagnostics
    photos: PhotoStats


def prepare_book(
    project: Project, build_dir: Path, *, web: bool = False, qr: bool = True
) -> Prepared:
    """Resolve the published book and copy its media to portable ``assets/`` paths.

    ``web`` picks the website photo variant instead of the print one. ``qr=False``
    leaves QR codes out, for formats read on the device that would scan them.
    """
    loaded = load(project)
    if not loaded.diagnostics.ok:
        raise ValidationFailed(loaded.diagnostics)
    model = resolve(
        loaded.settings,
        loaded.content,
        loaded.shortlinks.links,
        content_root=project.content_root,
    )
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)
    media, photos = build_media(
        project,
        model,
        build_dir,
        loaded.diagnostics,
        loaded.settings.book.photos.web if web else loaded.settings.book.photos.print,
    )
    if not loaded.diagnostics.ok:
        raise ValidationFailed(loaded.diagnostics)
    assets = build_dir / "assets"
    assets.mkdir()
    maps = []
    for mapping in (media.qr if qr else {}, media.images):
        copied = {}
        for label, relative in mapping.items():
            source = (build_dir / relative).resolve()
            name = f"{html_id(label)}{source.suffix}"
            if mapping is media.qr:
                name = f"qr-{name}"
            shutil.copyfile(source, assets / name)
            copied[label] = f"assets/{name}"
        maps.append(copied)
    portable = Media(qr=maps[0], images=maps[1], image_sizes=media.image_sizes)
    return Prepared(model, portable, loaded.diagnostics, photos)


def descriptions(model: BookModel) -> dict[str, str | None]:
    """Each published recipe's and component's description, by label."""
    found: dict[str, str | None] = {recipe_label(r.id): r.meta.description for r in model.recipes}
    found.update({component_label(c.id): c.meta.description for c in model.components})
    return found
