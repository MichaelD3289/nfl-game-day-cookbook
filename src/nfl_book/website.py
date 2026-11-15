"""Independent HTML presentation of the resolved book; never mutates authored content."""

from __future__ import annotations

import html
import shutil
import subprocess
import tomllib
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
from nfl_book.pipeline import load
from nfl_book.project import Project
from nfl_book.publishing import EPUB_FILENAME, RELEASES
from nfl_book.references import html_id, menu_label, page_source, recipe_label
from nfl_book.render.pages import PageSpec, build_pages, menu_view
from nfl_book.render.views import CoverView, DivisionView, IndexView, ItemView, view_fields
from nfl_book.website_pages import RecipeCard, WebRecipeView, marked, site_builders


@dataclass(frozen=True)
class WebsiteResult:
    document: Path
    site: Path | None
    diagnostics: Diagnostics
    photos: PhotoStats = field(default_factory=PhotoStats)


def _filename(page: PageSpec) -> str:
    return page_source(page.slug)


def _scalable(item: ItemView) -> str:
    """Ingredient Markdown with each scalable amount wrapped for website-scale.js."""
    return marked(item.text, item.amounts)


def _navigation(pages: list[PageSpec]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = [
        {"text": "Start here", "href": "index.qmd"},
        {"text": "All recipes", "href": "contents.qmd"},
        {"text": "Browse recipes", "href": "browse.qmd"},
    ]
    indexes = [
        {"text": p.view.title, "href": _filename(p)} for p in pages if isinstance(p.view, IndexView)
    ]
    result.append({"section": "Find a recipe", "contents": indexes})
    for p in pages:
        if isinstance(p.view, DivisionView):
            teams = [
                {"text": t.name, "href": f"{_filename(p)}#{html_id(t.label)}"}
                for t in p.view.teams
                if t.recipes
            ]
            if teams:
                result.append({"section": p.view.name, "href": _filename(p), "contents": teams})
    result.extend(
        [
            {"text": "Game Day Menus", "href": "game-day-menus.qmd"},
            {"text": "Build your own menu", "href": "menu-builder.qmd"},
            {"text": "Matchup menu", "href": "matchup.qmd"},
            {"text": "Make It or Buy It", "href": "make-it-or-buy-it.qmd"},
        ]
    )
    return result


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


def build_website(project: Project, *, render: bool = True, preview: str = "") -> WebsiteResult:
    """Build the site; ``preview`` labels an unreleased build (a branch and commit) on
    every page, so it cannot pass for the published edition."""
    build_dir = project.generated_dir / "site"
    metadata = tomllib.loads((project.root / "pyproject.toml").read_text())
    version = metadata["project"]["version"]
    prepared = prepare_book(project, build_dir, web=True)
    model, diags, photos = prepared.model, prepared.diagnostics, prepared.photos
    catalog = recipe_catalog(model, prepared.media, edition=version)
    pages = build_pages(model, prepared.media, site_builders(model, prepared.media, catalog))
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
    book = load(project).settings.book
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
    resources = [
        "assets/**",
        "scale.js",
        "print.js",
        "shop.js",
        CATALOG_FILE,
        "browse.js",
        "menu.js",
        "matchup.js",
        "cook.js",
        "timeline.js",
    ]
    write_catalog(catalog, build_dir / CATALOG_FILE)
    shutil.copyfile(project.styles_dir / "website-browse.js", build_dir / "browse.js")
    shutil.copyfile(project.styles_dir / "website-scale.js", build_dir / "scale.js")
    shutil.copyfile(project.styles_dir / "website-print.js", build_dir / "print.js")
    shutil.copyfile(project.styles_dir / "website-shop.js", build_dir / "shop.js")
    shutil.copyfile(project.styles_dir / "website-menu.js", build_dir / "menu.js")
    shutil.copyfile(project.styles_dir / "website-matchup.js", build_dir / "matchup.js")
    shutil.copyfile(project.styles_dir / "website-cook.js", build_dir / "cook.js")
    shutil.copyfile(project.styles_dir / "website-timeline.js", build_dir / "timeline.js")
    scripts = ["print.js", "shop.js", "cook.js", "timeline.js"]
    html_format: dict[str, Any] = {
        "theme": ["cosmo", "website.scss"],
        "css": ["website.css", "roadtrip.css"],
        "grid": {"body-width": "1280px", "margin-width": "0px", "gutter-width": "1.5rem"},
        "toc": False,
        "anchor-sections": False,
        "smooth-scroll": True,
        "lang": "en",
    }
    if book.suggestion_form_url:
        resources.append("suggest.js")
        scripts.append("suggest.js")
        shutil.copyfile(project.styles_dir / "website-suggest.js", build_dir / "suggest.js")
    if preview:
        html_format["include-before-body"] = {
            "text": '<div class="preview-banner" role="note"><strong>Preview</strong> '
            f"{html.escape(preview)}. Not a published edition: the version and download "
            "links point to the latest release.</div>"
        }
    html_format["include-after-body"] = {
        "text": "\n".join(f'<script src="{name}"></script>' for name in scripts)
    }
    cover = pages[0].view
    assert isinstance(cover, CoverView)
    config = {
        "project": {
            "type": "website",
            "output-dir": "_site",
            "render": ["*.qmd"],
            "resources": resources,
        },
        "website": {
            "title": cover.title,
            "search": {"location": "navbar", "type": "overlay"},
            "navbar": {
                "collapse-below": "lg",
                "left": [
                    {"text": "Browse recipes", "href": "browse.qmd"},
                    {"text": "Game Day Menus", "href": "game-day-menus.qmd"},
                    {"text": "Build your own menu", "href": "menu-builder.qmd"},
                    {"text": "Matchup menu", "href": "matchup.qmd"},
                    {
                        "text": "Explore",
                        "menu": [
                            {"text": "Make It or Buy It", "href": "make-it-or-buy-it.qmd"},
                            {"text": "All recipes by team", "href": "contents.qmd"},
                            *[
                                {
                                    "text": item.get("text", item.get("section", "")),
                                    "href": item["href"],
                                }
                                for group in _navigation(pages)
                                for item in (
                                    group.get("contents", [])
                                    if group.get("section") == "Find a recipe"
                                    else [group]
                                    if group.get("section")
                                    else []
                                )
                                if "href" in item
                            ],
                        ],
                    },
                ],
                "right": [
                    {
                        "text": "Downloads",
                        "menu": [
                            {"text": "Download PDF", "href": download},
                            {
                                "text": "Download EPUB",
                                "href": f"{RELEASES}/download/v{version}/{EPUB_FILENAME}",
                            },
                            {"text": "All formats & recipe cards", "href": RELEASES + "/latest"},
                            {"text": "All versions", "href": "versions.qmd"},
                            {"text": "Earlier releases", "href": RELEASES},
                            {"text": f"v{version}", "href": f"{RELEASES}/tag/v{version}"},
                        ],
                    },
                ],
            },
            "page-footer": {
                "left": "NFL Meals · A city-by-city game-day cookbook",
                "right": f"Preview {html.escape(preview)}"
                if preview
                else f"Edition {html.escape(version)}",
            },
        },
        "format": {"html": html_format},
    }
    (build_dir / "_quarto.yml").write_text(yaml.safe_dump(config, sort_keys=False))
    shutil.copyfile(project.styles_dir / "website.css", build_dir / "website.css")
    shutil.copyfile(project.styles_dir / "website-roadtrip.css", build_dir / "roadtrip.css")
    shutil.copyfile(project.styles_dir / "website.scss", build_dir / "website.scss")
    if not render:
        return WebsiteResult(build_dir / "index.qmd", None, diags, photos)
    quarto = shutil.which("quarto")
    if quarto is None:
        diags.error(
            "website",
            "Quarto is required; install it or use website --no-render.",
            build_dir / "_quarto.yml",
        )
        raise ValidationFailed(diags)
    compiled = subprocess.run(
        [quarto, "render", "--to", "html"],
        cwd=build_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    staged = build_dir / "_site"
    if compiled.returncode:
        tail = "\n".join((compiled.stdout + compiled.stderr).splitlines()[-35:])
        diags.error("website", f"Quarto HTML build failed:\n{tail}", build_dir / "_quarto.yml")
        raise ValidationFailed(diags)
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
