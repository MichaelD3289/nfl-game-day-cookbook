"""The resolved book and portable media shared by the digital formats."""

import shutil
from dataclasses import replace
from pathlib import Path

from nfl_book.edition import Edition, published_edition
from nfl_book.project import Project
from nfl_book.references import component_label, html_id, recipe_label
from nfl_book.render.pages import Media
from nfl_book.resolve import BookModel


def prepare_book(
    project: Project, build_dir: Path, *, web: bool = False, qr: bool = True
) -> Edition:
    """The published edition with its media copied to portable ``assets/`` paths.

    ``web`` picks the website photo variant instead of the print one. ``qr=False``
    leaves QR codes out, for formats read on the device that would scan them.
    """
    edition = published_edition(project, build_dir, web=web, fresh=True)
    media = edition.media
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
    return replace(edition, media=portable)


def descriptions(model: BookModel) -> dict[str, str | None]:
    """Each published recipe's and component's description, by label."""
    found: dict[str, str | None] = {recipe_label(r.id): r.meta.description for r in model.recipes}
    found.update({component_label(c.id): c.meta.description for c in model.components})
    return found
