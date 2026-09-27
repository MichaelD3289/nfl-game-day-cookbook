"""Shared presentation contexts and portable media for digital formats."""

import shutil
from pathlib import Path

from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.images import PhotoStats
from nfl_book.pipeline import build_media, load
from nfl_book.project import Project
from nfl_book.references import html_id
from nfl_book.render.pages import Media, PageSpec, build_pages
from nfl_book.resolve import BookModel, resolve


def prepare_pages(
    project: Project, build_dir: Path, *, web: bool = False, qr: bool = True
) -> tuple[list[PageSpec], Diagnostics, PhotoStats, BookModel]:
    """Resolve the published book into page specs with portable ``assets/`` media.

    ``web`` picks the website photo variant instead of the print one. ``qr=False``
    leaves QR codes out, for formats read on the device that would scan them.
    """
    loaded = load(project)
    if not loaded.diagnostics.ok:
        raise ValidationFailed(loaded.diagnostics)
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
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
    pages = build_pages(model, Media(qr=maps[0], images=maps[1], image_sizes=media.image_sizes))
    descriptions = {f"recipe:{r.id}": r.meta.description for r in model.recipes}
    descriptions.update({f"component:{c.id}": c.meta.description for c in model.components})
    menu_previews = {m["label"]: m for page in pages for m in page.context.get("menus", [])}
    for page in pages:
        page.context["descriptions"] = descriptions
        page.context["menu_previews"] = menu_previews
    return pages, loaded.diagnostics, photos, model
