"""Stable-ID references: component markers and cross-reference labels.

Authors reference a component from an ingredient line with
``{{component:<component-id>}}``. The marker is removed from the displayed
text and replaced by the Q marker plus a page reference when rendered.

Every page-addressable item gets a LaTeX label derived from its stable ID;
LaTeX resolves page numbers from these labels at compile time.

:func:`address` is the one place that turns an item into everything that names it:
its label, page slug, page file, HTML id and website URL. Nothing else builds these.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from nfl_book import __version__
from nfl_book.models.common import SLUG_PATTERN
from nfl_book.models.content import (
    Component,
    DishOff,
    GameDayMenu,
    Ingredient,
    IngredientGroup,
    Recipe,
)
from nfl_book.models.nfl import Division, Team
from nfl_book.publication import is_published
from nfl_book.quantities import NO_SCALE_RE, find_amounts

MARKER_RE = re.compile(r"\{\{\s*component\s*:\s*(?P<id>[^{}\s]*)\s*\}\}")
BRACES_RE = re.compile(r"\{\{.*?\}\}")
BULLET_RE = re.compile(r"^[-*+]\s+(?P<text>.+)$")
GROUP_RE = re.compile(r"^###\s+(?P<title>.+?)\s*#*\s*$")
SLUG_RE = re.compile(SLUG_PATTERN)


def html_id(label: str) -> str:
    """The HTML id for a label in digital outputs (website, EPUB): ``recipe:x`` -> ``recipe-x``."""
    return label.replace(":", "-")


def recipe_label(recipe_id: str) -> str:
    return f"recipe:{recipe_id}"


def recipe_end_label(recipe_id: str) -> str:
    return f"recipe:{recipe_id}:end"


def component_label(component_id: str) -> str:
    return f"component:{component_id}"


def division_label(division_key: str) -> str:
    return f"division:{division_key}"


def division_end_label(division_key: str) -> str:
    return f"division:{division_key}:end"


def menu_label(menu_id: str) -> str:
    return f"menu:{menu_id}"


def menu_end_label(menu_id: str) -> str:
    return f"menu:{menu_id}:end"


def team_label(team_slug: str) -> str:
    return f"team:{team_slug}"


def section_label(section_id: str) -> str:
    return f"section:{section_id}"


def index_label(index_id: str) -> str:
    return f"index:{index_id}"


def kind_label(kind_id: str) -> str:
    """Label of a component-kind section (EPUB only): ``kind:<id>``."""
    return f"kind:{kind_id}"


LABEL_PREFIXES = (
    "recipe:",
    "component:",
    "division:",
    "menu:",
    "team:",
    "section:",
    "index:",
    "kind:",
)
"""Every label starts with one of these; the page map reads them back from the PDF."""


def edition_root(base: str) -> str:
    """This edition's copy of the website, which every release keeps at ``/vX.Y.Z/``."""
    return f"{base.rstrip('/')}/v{__version__}/"


def page_source(slug: str) -> str:
    """The Quarto page file for a slug. Cross-links inside Quarto use this form; Quarto
    rewrites it to ``.html``. The cover is the site's ``index``."""
    return f"{'index' if slug == 'cover' else slug}.qmd"


def page_url(slug: str) -> str:
    """The rendered page for a slug, for JS, QR codes, the catalog and print links."""
    return f"{'index' if slug == 'cover' else slug}.html"


def menu_page_slug(menu_type_id: str, number: int) -> str:
    """Page ``number`` (from 1) of the game-day menus of one type."""
    return f"menus-{menu_type_id}-{number}"


@dataclass(frozen=True)
class SectionPage:
    """A book section with its own page: contents, game-day menus, browse, ..."""

    id: str


@dataclass(frozen=True)
class IndexPage:
    """A search index page."""

    id: str


@dataclass(frozen=True)
class KindSection:
    """The EPUB section that opens a run of components of one kind."""

    id: str


@dataclass(frozen=True)
class Placed:
    """An item that is an anchor on a page it does not own: a team on its division's
    page, or a game-day menu on one of its type's pages (``page`` is that page's slug)."""

    item: Team | GameDayMenu
    page: str


Item = Recipe | Component | Division | DishOff | Placed | SectionPage | IndexPage | KindSection


@dataclass(frozen=True)
class Address:
    """Everything that names one labelled item.

    ``slug``, ``page_source`` and ``page_url`` name the page the item is on: its own
    page for a recipe, component, division, section or index, otherwise the page that
    holds it (a team or dish-off on its division's page, a menu on a menu page).
    ``html_id`` is the item's anchor on that page. ``edition_url`` is the item in this
    edition of the website, ``None`` when it is not published there: a draft, an item
    the website has no anchor for, or no ``website_url``.
    """

    kind: str
    label: str
    end_label: str | None
    slug: str
    page_source: str
    page_url: str
    html_id: str
    edition_url: str | None


def address(item: Item, *, website_url: str | None = None) -> Address:
    """The address of ``item``; ``website_url`` is ``book.website_url``, if set.

    This is the only status check outside ``resolve``: a draft has no ``edition_url``,
    because the website publishes published content only.
    """
    published = True
    anchored = True  # an anchor on the page, not the page itself
    on_website = True
    end: str | None = None
    match item:
        case Recipe():
            kind, label, slug = "recipe", recipe_label(item.id), f"recipe-{item.id}"
            end, anchored = recipe_end_label(item.id), False
            published = is_published(item.meta.status)
        case Component():
            kind, label, slug = "component", component_label(item.id), f"component-{item.id}"
            anchored, published = False, is_published(item.meta.status)
        case Division():
            kind, label, slug = "division", division_label(item.key), f"division-{item.key}"
            end, anchored = division_end_label(item.key), False
        case DishOff():
            kind, label, slug = "dish-off", menu_label(item.id), f"division-{item.division.key}"
            published = is_published(item.meta.status)
        case Placed(item=Team() as team, page=slug):
            kind, label = "team", team_label(team.slug)
        case Placed(item=GameDayMenu() as menu, page=slug):
            kind, label, end = "menu", menu_label(menu.id), menu_end_label(menu.id)
            published = is_published(menu.meta.status)
        case SectionPage():
            kind, label, slug = "section", section_label(item.id), item.id
            anchored = False
        case IndexPage():
            kind, label, slug = "index", index_label(item.id), f"index-{item.id}"
            anchored = False
        case KindSection():
            # A heading inside the EPUB's component run; the website has no such anchor.
            kind, label, slug = "kind", kind_label(item.id), "make-it-or-buy-it"
            on_website = False
    anchor = html_id(label)
    url = None
    if website_url and published and on_website:
        url = f"{edition_root(website_url)}{page_url(slug)}"
        url += f"#{anchor}" if anchored else ""
    return Address(kind, label, end, slug, page_source(slug), page_url(slug), anchor, url)


def find_markers(text: str) -> list[str]:
    """Any ``{{...}}`` constructs in free text (markers are illegal there)."""
    return BRACES_RE.findall(text)


def parse_ingredients(text: str) -> tuple[tuple[IngredientGroup, ...], list[str]]:
    """Parse an ``## Ingredients`` section.

    Accepts bullet lines, optionally grouped under ``### Subheading`` lines.
    Returns the groups plus human-readable problems (empty when valid).
    """
    problems: list[str] = []
    groups: list[tuple[str | None, list[Ingredient]]] = [(None, [])]
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if group := GROUP_RE.match(line):
            groups.append((group["title"], []))
            continue
        bullet = BULLET_RE.match(line)
        if not bullet:
            problems.append(
                f"Ingredients line {lineno}: expected '- item' or '### Group', got {line!r}"
            )
            continue
        item, item_problems = parse_ingredient(bullet["text"])
        problems.extend(f"Ingredients line {lineno}: {p}" for p in item_problems)
        if item:
            groups[-1][1].append(item)
    result = tuple(IngredientGroup(h, tuple(items)) for h, items in groups if items)
    for heading, items in groups:
        if heading is not None and not items:
            problems.append(f"Ingredients group {heading!r} has no items")
    if not result and not problems:
        problems.append("Ingredients section has no items")
    return result, problems


def parse_ingredient(text: str) -> tuple[Ingredient | None, list[str]]:
    fixed = len(NO_SCALE_RE.findall(text))
    braces = BRACES_RE.findall(text)
    markers = list(MARKER_RE.finditer(text))
    problems = []
    if fixed > 1:
        problems.append("only one {{no-scale}} marker is allowed per ingredient line")
    if len(braces) != len(markers) + fixed:
        bad = [b for b in braces if not (MARKER_RE.fullmatch(b) or NO_SCALE_RE.fullmatch(b))]
        problems.append(
            f"malformed marker {bad[0]!r}; use {{{{component:<component-id>}}}} or {{{{no-scale}}}}"
        )
    if len(markers) > 1:
        problems.append("only one component reference is allowed per ingredient line")
    component = None
    if markers:
        component = markers[0]["id"]
        if not SLUG_RE.match(component):
            problems.append(f"invalid component id {component!r} in reference")
    display = " ".join(NO_SCALE_RE.sub(" ", MARKER_RE.sub(" ", text)).split())
    if not display:
        problems.append("ingredient needs text besides the component reference")
    amounts, amount_problems = find_amounts(display)
    if fixed and not amounts and not amount_problems:
        problems.append("{{no-scale}} is only needed on a line with an amount; remove it")
    if not fixed:
        problems.extend(f"{p} (or mark the line {{{{no-scale}}}})" for p in amount_problems)
    if problems:
        return None, problems
    return Ingredient(display, component, () if fixed else amounts), []
