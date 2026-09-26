"""Render one recipe or component on its own, fast, for authoring.

Page references use the last full build's page map (``generated/pagemap.json``)
and fall back to "--". Only errors in the previewed file block the preview.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from nfl_book.errors import BookError, Diagnostics, ValidationFailed
from nfl_book.pipeline import build_media, load
from nfl_book.postbuild import load_pagemap
from nfl_book.project import Project
from nfl_book.render import assemble, component_page, make_env, recipe_page
from nfl_book.render.env import tex
from nfl_book.render.pages import PageSpec
from nfl_book.render.quarto import render_pdf
from nfl_book.resolve import resolve


@dataclass
class PreviewResult:
    item_id: str
    document: Path
    pdf: Path | None = None
    diagnostics: Diagnostics = field(default_factory=Diagnostics)


def preview_preamble(pagemap: dict[str, int]) -> str:
    lines = ["\\BookPreviewtrue"]
    lines.extend(f"\\BookSetPreviewPage{{{label}}}{{{page}}}" for label, page in pagemap.items())
    return "\n".join(lines)


def preview(project: Project, path: Path, *, pdf: bool = True) -> PreviewResult:
    target = path.resolve()
    if not target.is_file():
        raise BookError(f"{path}: file not found")
    loaded = load(project, require_shortlinks=False)
    own = loaded.diagnostics.for_paths([target])
    if not own.ok:
        raise ValidationFailed(own)

    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    recipe = next((r for r in loaded.content.recipes if r.path.resolve() == target), None)
    component = next((c for c in loaded.content.components if c.path.resolve() == target), None)
    item = recipe or component
    if item is None:
        raise BookError(f"{path}: not a recipe or component (only those can be previewed)")

    build_dir = project.preview_build_dir / item.id
    media = build_media(project, model, build_dir)
    spec: PageSpec = (
        recipe_page(model, recipe, media)
        if recipe is not None
        else component_page(model, item, media)  # type: ignore[arg-type]
    )
    if item.meta.source and item.meta.source.url not in loaded.shortlinks:
        own.warning("shortlink", "no cached short URL: previewing without a QR code", target)
    assembled = assemble(
        make_env(project.templates_dir),
        [spec],
        build_dir,
        title=tex(item.title),
        paper=loaded.settings.book.paper,
        styles_dir=project.styles_dir,
        preamble=preview_preamble(load_pagemap(project.pagemap_file)),
    )
    result = PreviewResult(item.id, assembled.document, diagnostics=own)
    if pdf:
        result.pdf = render_pdf(assembled.document)
    return result
