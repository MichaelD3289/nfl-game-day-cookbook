"""The website's navigation, its asset table and its Quarto project config.

Everything here is data or a pure function, so the site's shape is decided in one place:
add a script to :data:`ASSETS` and it is copied, listed as a project resource and loaded
by a script tag.
"""

from __future__ import annotations

import html
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from nfl_book.catalog import CATALOG_FILE
from nfl_book.publishing import EPUB_FILENAME, RELEASES
from nfl_book.references import page_source
from nfl_book.render.pages import PageSpec
from nfl_book.render.views import DivisionView, IndexView


@dataclass(frozen=True)
class SiteAsset:
    """A file at the site root. ``source`` is its name in ``styles/`` (None when the build
    generates it). ``script`` adds a script tag to every page; ``needs_suggestions`` keeps
    it out of sites without a suggestion form."""

    name: str
    source: str | None
    script: bool = False
    needs_suggestions: bool = False


# Order is the order of the project's resources and of the script tags.
ASSETS: tuple[SiteAsset, ...] = (
    SiteAsset("scale.js", "website-scale.js"),
    SiteAsset("print.js", "website-print.js", script=True),
    SiteAsset("shop.js", "website-shop.js", script=True),
    SiteAsset(CATALOG_FILE, None),
    SiteAsset("browse.js", "website-browse.js"),
    SiteAsset("menu.js", "website-menu.js"),
    SiteAsset("matchup.js", "website-matchup.js"),
    SiteAsset("cook.js", "website-cook.js", script=True),
    SiteAsset("timeline.js", "website-timeline.js", script=True),
    SiteAsset("suggest.js", "website-suggest.js", script=True, needs_suggestions=True),
)

# Stylesheets the theme loads, copied beside the pages: (name on the site, name in styles/).
STYLES: tuple[tuple[str, str], ...] = (
    ("website.css", "website.css"),
    ("roadtrip.css", "website-roadtrip.css"),
    ("website.scss", "website.scss"),
)


def active_assets(suggestions: bool) -> tuple[SiteAsset, ...]:
    return tuple(a for a in ASSETS if suggestions or not a.needs_suggestions)


@dataclass(frozen=True)
class NavLink:
    text: str
    href: str


@dataclass(frozen=True)
class Navigation:
    """``primary`` links sit in the navbar; ``explore`` fills its Explore menu."""

    primary: tuple[NavLink, ...]
    explore: tuple[NavLink, ...]


def navigation(pages: Sequence[PageSpec]) -> Navigation:
    indexes = [
        NavLink(p.view.title, page_source(p.slug)) for p in pages if isinstance(p.view, IndexView)
    ]
    divisions = [
        NavLink(p.view.name, page_source(p.slug))
        for p in pages
        if isinstance(p.view, DivisionView) and any(t.recipes for t in p.view.teams)
    ]
    return Navigation(
        primary=(
            NavLink("Browse recipes", "browse.qmd"),
            NavLink("Game Day Menus", "game-day-menus.qmd"),
            NavLink("Build your own menu", "menu-builder.qmd"),
            NavLink("Matchup menu", "matchup.qmd"),
        ),
        explore=(
            NavLink("Make It or Buy It", "make-it-or-buy-it.qmd"),
            NavLink("All recipes by team", "contents.qmd"),
            *indexes,
            *divisions,
        ),
    )


def _link(link: NavLink) -> dict[str, str]:
    return {"text": link.text, "href": link.href}


def quarto_config(
    *,
    title: str,
    nav: Navigation,
    assets: Sequence[SiteAsset],
    version: str,
    download: str,
    preview: str = "",
) -> dict[str, Any]:
    """The site's ``_quarto.yml`` as data."""
    html_format: dict[str, Any] = {
        "theme": ["cosmo", "website.scss"],
        "css": ["website.css", "roadtrip.css"],
        "grid": {"body-width": "1280px", "margin-width": "0px", "gutter-width": "1.5rem"},
        "toc": False,
        "anchor-sections": False,
        "smooth-scroll": True,
        "lang": "en",
    }
    if preview:
        html_format["include-before-body"] = {
            "text": '<div class="preview-banner" role="note"><strong>Preview</strong> '
            f"{html.escape(preview)}. Not a published edition: the version and download "
            "links point to the latest release.</div>"
        }
    html_format["include-after-body"] = {
        "text": "\n".join(f'<script src="{a.name}"></script>' for a in assets if a.script)
    }
    return {
        "project": {
            "type": "website",
            "output-dir": "_site",
            "render": ["*.qmd"],
            "resources": ["assets/**", *(a.name for a in assets)],
        },
        "website": {
            "title": title,
            "search": {"location": "navbar", "type": "overlay"},
            "navbar": {
                "collapse-below": "lg",
                "left": [
                    *(_link(link) for link in nav.primary),
                    {"text": "Explore", "menu": [_link(link) for link in nav.explore]},
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
