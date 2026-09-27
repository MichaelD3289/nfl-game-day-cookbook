"""Offline recipe-card PDF, independent of the one-page cookbook layout."""

from __future__ import annotations

import json
import shutil

from nfl_book.errors import ValidationFailed
from nfl_book.pipeline import BuildResult, build_media, load
from nfl_book.postbuild import check_manifest, read_pagemap, write_pagemap
from nfl_book.project import Project
from nfl_book.render import make_env
from nfl_book.render.assemble import front_matter, write_if_changed
from nfl_book.render.env import tex
from nfl_book.render.pages import recipe_context, web_href
from nfl_book.render.quarto import render_pdf, scan_log
from nfl_book.resolve import resolve


def build_cards(project: Project, *, pdf: bool = True, strict: bool = False) -> BuildResult:
    """Render published recipes to flowing cards, with no booklet page references."""
    loaded = load(project)
    diags = loaded.diagnostics
    if not diags.ok:
        raise ValidationFailed(diags)
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    settings = loaded.settings.book.cards
    build_dir = project.generated_dir / "cards"
    media, photos = build_media(project, model, build_dir, diags, loaded.settings.book.photos.print)
    if not diags.ok:
        raise ValidationFailed(diags)
    pages_dir = build_dir / "pages"
    if pages_dir.exists():
        shutil.rmtree(pages_dir)
    pages_dir.mkdir(parents=True)
    includes = []
    for name in ("theme.tex", "cards.tex"):
        target = build_dir / "styles" / name
        source = project.styles_dir / name
        try:
            style = source.read_text(encoding="utf-8")
        except OSError as exc:
            diags.error("cards-style", f"cannot read card style: {exc}", source)
            continue
        write_if_changed(target, style)
        includes.append(f"styles/{name}")
    if not diags.ok:
        raise ValidationFailed(diags)
    geometry = (
        f"\\geometry{{paperwidth={float(settings.width_inches)}in,"
        f"paperheight={float(settings.height_inches)}in,"
        r"margin=\CardMargin,headheight=\CardHeadHeight,headsep=\CardHeadSep}"
    )
    write_if_changed(build_dir / "styles" / "card-geometry.tex", geometry + "\n")
    includes.append("styles/card-geometry.tex")
    env = make_env(project.templates_dir)
    names = []
    manifest = []
    for recipe in model.recipes:
        context = recipe_context(model, recipe, media)
        context["component_links"] = {
            f"component:{c.id}": {"title": c.title, "href": web_href(c, "component", model)}
            for c in model.components
        }
        name = f"pages/recipe-{recipe.id}.qmd"
        write_if_changed(
            build_dir / name, env.get_template("cards/recipe.qmd.j2").render(**context)
        )
        names.append(name)
        manifest.append(
            {
                "file": name,
                "source": str(recipe.path),
                "anchors": [context["label"], context["end_label"]],
                "spans": [[context["label"], context["end_label"]]],
            }
        )
    document = build_dir / "cards.qmd"
    write_if_changed(
        document,
        env.get_template("book.qmd.j2").render(
            front_matter=front_matter(
                tex(loaded.settings.book.title), "letter", includes, "", latex_auto_install=False
            ),
            pages=names,
        ),
    )
    write_if_changed(build_dir / "manifest.json", json.dumps({"pages": manifest}, indent=2) + "\n")
    result = BuildResult(document, diagnostics=diags, photos=photos)
    if not pdf:
        return result
    compiled = render_pdf(document)
    scan_log(document.with_suffix(".log"), diags)
    pagemap = read_pagemap(compiled)
    write_pagemap(pagemap, build_dir / "pagemap.json")
    check_manifest(
        build_dir / "manifest.json", pagemap, diags, strict=strict, max_pages=settings.max_pages
    )
    if not diags.ok:
        raise ValidationFailed(diags)
    project.dist_dir.mkdir(parents=True, exist_ok=True)
    result.pdf = project.dist_dir / settings.output_filename
    shutil.copyfile(compiled, result.pdf)
    return result
