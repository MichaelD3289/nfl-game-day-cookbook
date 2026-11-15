"""Offline recipe-card PDF, independent of the one-page cookbook layout."""

from __future__ import annotations

import shutil

from nfl_book.edition import published_edition
from nfl_book.errors import ValidationFailed
from nfl_book.pipeline import BuildResult
from nfl_book.postbuild import check_manifest, read_pagemap, write_pagemap
from nfl_book.project import Project
from nfl_book.references import address, component_label
from nfl_book.render import PageSpec, assemble, make_env
from nfl_book.render.assemble import Layout
from nfl_book.render.env import tex
from nfl_book.render.pages import recipe_view
from nfl_book.render.quarto import Quarto, QuartoCli, render_pdf, scan_log
from nfl_book.render.views import CardView, ComponentLink, view_fields


def build_cards(
    project: Project,
    *,
    pdf: bool = True,
    strict: bool = False,
    quarto: Quarto | None = None,
) -> BuildResult:
    """Render published recipes to flowing cards, with no booklet page references."""
    build_dir = project.generated_dir / "cards"
    edition = published_edition(project, build_dir)
    model, diags = edition.model, edition.diagnostics
    settings = edition.settings.book.cards
    links = {
        component_label(c.id): ComponentLink(
            c.title, address(c, edition=edition.settings.edition_root).edition_url
        )
        for c in model.components
    }
    specs = []
    for recipe in model.recipes:
        card = CardView(
            **view_fields(recipe_view(model, recipe, edition.media)),
            component_links=links,
            recipe_file=str(recipe.path),
        )
        assert card.end_label is not None
        specs.append(
            PageSpec(
                f"recipe-{recipe.id}",
                "cards/recipe.qmd.j2",
                card,
                anchors=(card.label,),
                spans=((card.label, card.end_label),),
            )
        )
    geometry = (
        f"\\geometry{{paperwidth={float(settings.width_inches)}in,"
        f"paperheight={float(settings.height_inches)}in,"
        r"margin=\CardMargin,headheight=\CardHeadHeight,headsep=\CardHeadSep}"
    )
    assembled = assemble(
        make_env(project.templates_dir),
        specs,
        build_dir,
        title=tex(edition.settings.book.title),
        paper="letter",
        styles_dir=project.styles_dir,
        diagnostics=diags,
        layout=Layout(
            document="cards.qmd",
            styles=("theme.tex", "cards.tex"),
            numbered=False,
            latex_auto_install=False,
            extra_styles={"card-geometry.tex": geometry + "\n"},
        ),
    )
    result = BuildResult(assembled.document, diagnostics=diags, photos=edition.photos)
    if not pdf:
        return result
    compiled = render_pdf(quarto or QuartoCli(), assembled.document, diags)
    scan_log(assembled.document.with_suffix(".log"), diags)
    pagemap = read_pagemap(compiled)
    write_pagemap(pagemap, build_dir / "pagemap.json")
    check_manifest(assembled.manifest, pagemap, diags, strict=strict, max_pages=settings.max_pages)
    if not diags.ok:
        raise ValidationFailed(diags)
    project.dist_dir.mkdir(parents=True, exist_ok=True)
    result.pdf = project.dist_dir / settings.output_filename
    shutil.copyfile(compiled, result.pdf)
    return result
