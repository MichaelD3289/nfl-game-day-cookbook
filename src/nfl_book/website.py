"""Independent HTML presentation of the resolved book; never mutates authored content."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from nfl_book.catalog import CATALOG_FILE, Catalog, recipe_catalog, write_catalog
from nfl_book.digital import descriptions, prepare_book
from nfl_book.digital_text import (
    WEBSITE_Q_MARK,
    digital_prose,
    escape_markdown,
    separate_fences,
    site_name,
)
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.images import PhotoStats
from nfl_book.project import Project
from nfl_book.publishing import RELEASES
from nfl_book.references import html_id, menu_label, page_source, recipe_label
from nfl_book.render.pages import PageSpec, build_pages, menu_view
from nfl_book.render.quarto import Quarto, QuartoCli, run_quarto
from nfl_book.render.views import CoverView, ItemView, view_fields
from nfl_book.site_config import STYLES, active_assets, navigation, quarto_config
from nfl_book.website_pages import RecipeCard, WebRecipeView, marked, site_builders


@dataclass(frozen=True)
class WebsiteResult:
    document: Path
    site: Path | None
    diagnostics: Diagnostics
    photos: PhotoStats = field(default_factory=PhotoStats)


def _filename(page: PageSpec) -> str:
    return page_source(page.slug)


def cover_title(pages: list[PageSpec]) -> str:
    cover = pages[0].view
    assert isinstance(cover, CoverView)
    return cover.title


def _scalable(item: ItemView) -> str:
    """Ingredient Markdown with each scalable amount wrapped for website-scale.js."""
    return marked(item.text, item.amounts)


def _discovery(catalog: Catalog) -> dict[str, Any]:
    """Website-only card data and a small, diverse introduction to the published book."""
    times = {o.id: o.label for f in catalog.facets if f.id == "practical-time" for o in f.options}
    cards = {}
    for recipe in catalog.recipes:
        labels = [times[value] for value in recipe.facets.get("practical-time", ())]
        cards[recipe_label(recipe.id)] = RecipeCard(
            **view_fields(recipe), time_label=" · ".join(labels)
        )
    recipes = list(cards.values())
    featured: list[RecipeCard] = []
    divisions: set[str] = set()
    for course in ("meals", "appetizers", "sides", "desserts", None, None, None, None):
        candidates = [
            r for r in recipes if r not in featured and (course is None or r.course == course)
        ]
        if candidates and len(featured) < 4:
            chosen = max(candidates, key=lambda r: (bool(r.photo), r.division not in divisions))
            featured.append(chosen)
            divisions.add(chosen.division)
    photos = [r for r in featured if r.photo]
    courses = next((f.options for f in catalog.facets if f.id == "course"), ())
    return {
        "recipe_cards": cards,
        "featured_recipes": featured,
        "hero_photos": photos[:2],
        "menu_photo": photos[-1] if photos else None,
        "course_links": courses,
    }


def build_website(
    project: Project, *, render: bool = True, preview: str = "", quarto: Quarto | None = None
) -> WebsiteResult:
    """Build the site; ``preview`` labels an unreleased build (a branch and commit) on
    every page, so it cannot pass for the published edition."""
    build_dir = project.generated_dir / "site"
    edition = prepare_book(project, build_dir, web=True)
    model, diags, photos, version = (
        edition.model,
        edition.diagnostics,
        edition.photos,
        edition.version,
    )
    catalog = recipe_catalog(model, edition.media, edition=version)
    pages = build_pages(model, edition.media, site_builders(model, edition.media, catalog))
    if not diags.ok:
        raise ValidationFailed(diags)
    routes = {label: f"{_filename(p)}#{html_id(label)}" for p in pages for label in p.anchors}
    env = Environment(
        loader=FileSystemLoader(project.templates_dir / "website"),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters.update(
        md=escape_markdown,
        web_body=lambda text: digital_prose(text, WEBSITE_Q_MARK),
        anchor=html_id,
        scalable=_scalable,
        site_name=site_name,
    )
    book = edition.settings.book
    env.globals.update(
        route=lambda label: routes[label],
        suggestion_form_url=book.suggestion_form_url,
        descriptions=descriptions(model),
        menu_previews={menu_label(m.id): menu_view(model, m) for m in model.menus},
        **_discovery(catalog),
    )
    pdf = book.output_filename
    download = f"{RELEASES}/latest/download/{pdf}"
    for page in pages:
        view = page.view
        head = view.head if isinstance(view, WebRecipeView) else ""
        matter: dict[str, Any] = {"title": "", "pagetitle": view.page_title}
        if head:
            matter["include-in-header"] = {"text": head}
        front = yaml.safe_dump(matter, sort_keys=False)
        body = env.get_template(page.template).render(
            **view_fields(view), version=version, download=download
        )
        (build_dir / _filename(page)).write_text(f"---\n{front}---\n\n{separate_fences(body)}")
    # The release workflow lists every published website version at the marker.
    (build_dir / "versions.qmd").write_text(
        '---\ntitle: ""\npagetitle: All versions\n---\n\n# All versions\n\n'
        "Each release of this cookbook stays online at its own address. Every edition's "
        f"PDF and downloadable website are also on [GitHub releases]({RELEASES}).\n\n"
        "```{=html}\n<!-- site-versions -->\n```\n"
    )
    assets = active_assets(bool(book.suggestion_form_url))
    write_catalog(catalog, build_dir / CATALOG_FILE)
    for asset in assets:
        if asset.source is not None:
            shutil.copyfile(project.styles_dir / asset.source, build_dir / asset.name)
    config = quarto_config(
        title=cover_title(pages),
        nav=navigation(pages),
        assets=assets,
        version=version,
        download=download,
        preview=preview,
    )
    (build_dir / "_quarto.yml").write_text(yaml.safe_dump(config, sort_keys=False))
    for name, source in STYLES:
        shutil.copyfile(project.styles_dir / source, build_dir / name)
    if not render:
        return WebsiteResult(build_dir / "index.qmd", None, diags, photos)
    config_file = build_dir / "_quarto.yml"
    if not run_quarto(
        quarto or QuartoCli(),
        build_dir,
        ["render", "--to", "html"],
        source=config_file,
        diagnostics=diags,
        code="website",
        what="website",
        skip="--no-render",
    ):
        raise ValidationFailed(diags)
    staged = build_dir / "_site"
    if not (staged / "index.html").is_file():
        diags.error(
            "website",
            "Quarto finished but rendered no pages (no _site/index.html); check that "
            "project.render in _quarto.yml lists the site's pages.",
            build_dir / "_quarto.yml",
        )
        raise ValidationFailed(diags)
    from nfl_book.website_check import check_site

    check_site(staged, diags)
    if not diags.ok:
        raise ValidationFailed(diags)
    target = project.dist_dir / "site"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(staged, target)
    return WebsiteResult(build_dir / "index.qmd", target, diags, photos)
