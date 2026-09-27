"""Turn the resolved :class:`BookModel` into an ordered list of page specs.

Each :class:`PageSpec` names a Jinja template, the view data it renders and
the LaTeX labels it is expected to anchor. Views hold labels, never page
numbers: every number in the book is resolved by LaTeX from those labels.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from nfl_book import __version__
from nfl_book.errors import Diagnostics
from nfl_book.models.content import Component, IngredientGroup, Recipe
from nfl_book.quantities import Amount
from nfl_book.references import (
    component_label,
    division_label,
    index_label,
    menu_label,
    recipe_end_label,
    recipe_label,
    section_label,
    team_label,
)
from nfl_book.resolve import BookModel, QuickOption, menu_recipes, quick_options_for
from nfl_book.validation import is_published

CONTENTS = section_label("contents")
GAME_DAY = section_label("game-day-menus")
MAKE_BUY = section_label("make-it-or-buy-it")
MENUS_PER_PAGE = 2


@dataclass(frozen=True)
class Media:
    """Paths (relative to the QMD build directory) of generated binary assets."""

    qr: Mapping[str, str] = field(default_factory=dict)  # "<kind>:<id>" -> path
    images: Mapping[str, str] = field(default_factory=dict)  # "<kind>:<id>" -> path
    image_sizes: Mapping[str, int] = field(default_factory=dict)  # square side in px


@dataclass(frozen=True)
class PageSpec:
    slug: str
    template: str
    context: dict[str, Any]
    anchors: tuple[str, ...] = ()
    spans: tuple[tuple[str, str], ...] = ()  # (start label, end label) expected on one page


# --------------------------------------------------------------------------- views
@dataclass(frozen=True)
class Ref:
    label: str
    title: str
    note: str = ""


@dataclass(frozen=True)
class ItemView:
    text: str  # Markdown
    ref: str | None  # component label when the line references a component
    amounts: tuple[Amount, ...] = ()  # scalable amounts in ``text`` (website only)


@dataclass(frozen=True)
class GroupView:
    heading: str | None
    items: tuple[ItemView, ...]


@dataclass(frozen=True)
class SourceView:
    title: str
    href: str  # short link when cached (print), else the full URL
    display: str
    url: str  # always the full source URL, for formats with clickable links


@dataclass(frozen=True)
class WebView:
    target: str  # slug of the website page it opens, e.g. "recipe-<id>"
    href: str
    edition: str


@dataclass(frozen=True)
class OptionView:
    label: str
    title: str
    text: str


# Past this many ingredient lines a bulleted list cannot share a page with the
# instructions, so groups are set as run-in paragraphs (as in the print booklet).
COMPACT_INGREDIENTS_OVER = 24


def _compact(groups: Iterable[IngredientGroup]) -> bool:
    return sum(len(g.items) for g in groups) > COMPACT_INGREDIENTS_OVER


def _groups(groups: Iterable[IngredientGroup]) -> list[GroupView]:
    return [
        GroupView(
            g.heading,
            tuple(
                ItemView(i.text, component_label(i.component) if i.component else None, i.amounts)
                for i in g.items
            ),
        )
        for g in groups
    ]


def _options(options: Sequence[QuickOption]) -> list[OptionView]:
    return [OptionView(component_label(o.component.id), o.component.title, o.text) for o in options]


def _source(item: Recipe | Component, model: BookModel) -> SourceView | None:
    source = item.meta.source
    if source is None:
        return None
    short = model.shortlinks.get(source.url)
    return SourceView(
        title=source.title or "",
        href=short or source.url,
        display=short or source.url,
        url=source.url,
    )


def _edition_root(base: str) -> str:
    """This edition's copy of the website, which every release keeps at ``/vX.Y.Z/``."""
    return f"{base.rstrip('/')}/v{__version__}/"


def web_href(item: Recipe | Component, kind: str, model: BookModel) -> str | None:
    """The item's page in this edition of the website, built from ``website_url``.

    Drafts have none: the website publishes only published content.
    """
    base = model.settings.book.website_url
    if not base or not is_published(item.meta.status):
        return None
    return f"{_edition_root(base)}{kind}-{item.id}.html"


def _web(item: Recipe | Component, kind: str, model: BookModel) -> WebView | None:
    href = web_href(item, kind, model)
    return None if href is None else WebView(f"{kind}-{item.id}", href, __version__)


def _meta(*parts: tuple[str, str | None]) -> list[tuple[str, str]]:
    return [(name, value) for name, value in parts if value]


def _meta_line(*parts: tuple[str, str | None]) -> str:
    return "   |   ".join(f"{name}: {value}" for name, value in _meta(*parts))


def _course(model: BookModel, recipe: Recipe) -> str:
    bucket = model.settings.course(recipe.meta.course)
    return bucket.singular if bucket else recipe.meta.course


def _recipe_ref(model: BookModel, recipe: Recipe, *, course: bool = False) -> Ref:
    note = recipe.team.short_name
    if course:
        note = f"{note}, {_course(model, recipe)}"
    return Ref(recipe_label(recipe.id), recipe.title, note)


# --------------------------------------------------------------------------- pages
def recipe_context(model: BookModel, recipe: Recipe, media: Media) -> dict[str, Any]:
    options = model.quick_options.get(recipe.id)
    if options is None:  # preview of unpublished content
        options = quick_options_for(recipe, model.components_by_id)
    return {
        "label": recipe_label(recipe.id),
        "end_label": recipe_end_label(recipe.id),
        "title": recipe.title,
        "team": recipe.team.name,
        "location": recipe.location,
        "course": _course(model, recipe),
        "division": recipe.division.name,
        "meta_line": _meta_line(
            ("Yield", recipe.meta.yield_), ("Prep", recipe.meta.prep), ("Cook", recipe.meta.cook)
        ),
        "meta": _meta(
            ("Yield", recipe.meta.yield_), ("Prep", recipe.meta.prep), ("Cook", recipe.meta.cook)
        ),
        "description": recipe.meta.description or "",
        "image": media.images.get(f"recipe:{recipe.id}", ""),
        "image_size": media.image_sizes.get(f"recipe:{recipe.id}", 0),
        "photo_credit": recipe.meta.photo_credit or "",
        "quick_options": _options(options),
        "groups": _groups(recipe.ingredients),
        "compact_ingredients": _compact(recipe.ingredients),
        "instructions": recipe.instructions,
        "kitchen_notes": recipe.kitchen_notes or "",
        "source": _source(recipe, model),
        "web": _web(recipe, "recipe", model),
        "qr": media.qr.get(f"recipe:{recipe.id}", ""),
    }


def component_context(model: BookModel, component: Component, media: Media) -> dict[str, Any]:
    usage = model.usage.get(component.id)
    used_in = [_recipe_ref(model, r) for r in usage.all] if usage else []
    return {
        "label": component_label(component.id),
        "title": component.title,
        "kind": component.kind.singular,
        "meta_line": _meta_line(("Yield", component.meta.yield_)),
        "meta": _meta(("Yield", component.meta.yield_)),
        "groups": _groups(component.ingredients),
        "method": component.method,
        "note": component.note or "",
        "quick_buy": component.meta.quick_buy,
        "used_in": used_in,
        "source": _source(component, model),
        "web": _web(component, "component", model),
        "qr": media.qr.get(f"component:{component.id}", ""),
    }


def _website(model: BookModel) -> dict[str, str] | None:
    base = model.settings.book.website_url
    if not base:
        return None
    href = _edition_root(base)
    return {"href": href, "display": href.removeprefix("https://"), "edition": __version__}


def check_web_links(model: BookModel, pages: Sequence[PageSpec], diags: Diagnostics) -> None:
    """Every website link printed in the book must open a page the website publishes.

    The website is built from these same page specs, so a link is valid exactly
    when its target is one of them.
    """
    slugs = {page.slug for page in pages}
    paths = {f"recipe-{r.id}": r.path for r in model.recipes_by_id.values()}
    paths.update({f"component-{c.id}": c.path for c in model.components_by_id.values()})
    for page in pages:
        web = page.context.get("web")
        if isinstance(web, WebView) and web.target not in slugs:
            diags.error(
                "web-link",
                f"links to {web.href}, but the website does not publish {web.target}",
                paths.get(page.slug),
            )


def _menu_view(model: BookModel, menu: Any) -> dict[str, Any]:
    return {
        "label": menu_label(menu.id),
        "title": menu.meta.title,
        "subtitle": getattr(menu.meta, "subtitle", None) or "",
        "recipes": [_recipe_ref(model, r, course=True) for r in menu_recipes(menu, model)],
        "why_it_works": getattr(menu.meta, "why_it_works", None) or "",
        "prep_plan": getattr(menu.meta, "prep_plan", None) or "",
        "description": getattr(menu.meta, "description", None) or "",
        "prep_note": getattr(menu.meta, "prep_note", None) or "",
    }


def _chunks(items: Sequence[Any], size: int) -> list[Sequence[Any]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def build_pages(model: BookModel, media: Media) -> list[PageSpec]:
    """The whole book, in publication order."""
    specs: list[PageSpec] = []
    recipes = model.recipes

    cover = model.cover
    specs.append(
        PageSpec(
            "cover",
            "cover.qmd.j2",
            {
                "title": (cover.title if cover else "") or model.settings.book.title,
                "subtitle": (cover.subtitle if cover else None)
                or model.settings.book.subtitle
                or "",
                "tagline": (cover.tagline if cover else None) or "",
                "body": cover.body if cover else "",
                "website": _website(model),
                "stats": {
                    "recipes": len(recipes),
                    "teams": len({r.team.slug for r in recipes}),
                    "components": len(model.components),
                    "menus": len(model.menus),
                },
            },
        )
    )

    specs.append(
        PageSpec(
            "contents",
            "contents.qmd.j2",
            {
                "label": CONTENTS,
                "indexes": [
                    Ref(index_label(i.definition.id), i.definition.title) for i in model.indexes
                ],
                "divisions": [
                    {
                        "ref": Ref(division_label(d.division.key), d.division.name),
                        "teams": [
                            {
                                "name": t.team.name,
                                "recipes": [_recipe_ref(model, r) for r in t.recipes],
                            }
                            for t in d.teams
                            if t.recipes
                        ],
                    }
                    for d in model.divisions
                ],
                "game_day": Ref(GAME_DAY, "Game Day Menus"),
                "make_buy": Ref(MAKE_BUY, "Make It or Buy It"),
            },
            anchors=(CONTENTS,),
        )
    )

    for resolved in model.indexes:
        definition = resolved.definition
        specs.append(
            PageSpec(
                f"index-{definition.id}",
                "index.qmd.j2",
                {
                    "label": index_label(definition.id),
                    "title": definition.title,
                    "intro": definition.config.intro or "",
                    "sections": [
                        {
                            "title": s.bucket.label,
                            "entries": [_recipe_ref(model, r) for r in s.recipes],
                        }
                        for s in resolved.sections
                    ],
                },
                anchors=(index_label(definition.id),),
            )
        )

    for section in model.divisions:
        division = section.division
        specs.append(
            PageSpec(
                f"division-{division.key}",
                "division.qmd.j2",
                {
                    "label": division_label(division.key),
                    "name": division.name,
                    "conference": division.conference_name,
                    "teams": [
                        {
                            "label": team_label(t.team.slug),
                            "name": t.team.name,
                            "location": t.team.location,
                            "recipes": [_recipe_ref(model, r, course=True) for r in t.recipes],
                        }
                        for t in section.teams
                    ],
                    "dishoffs": [_menu_view(model, d) for d in section.dishoffs],
                },
                anchors=(
                    division_label(division.key),
                    *(team_label(t.team.slug) for t in section.teams),
                ),
            )
        )
        for recipe in section.recipes:
            specs.append(recipe_page(model, recipe, media))

    specs.append(
        PageSpec(
            "game-day-menus",
            "game-day-index.qmd.j2",
            {
                "label": GAME_DAY,
                "groups": [
                    {
                        "title": g.menu_type.title,
                        "description": g.menu_type.description or "",
                        "menus": [
                            Ref(menu_label(m.id), m.meta.title, m.meta.subtitle or "")
                            for m in g.menus
                        ],
                    }
                    for g in model.menu_groups
                ],
            },
            anchors=(GAME_DAY,),
        )
    )
    for group in model.menu_groups:
        for n, chunk in enumerate(_chunks(group.menus, MENUS_PER_PAGE), start=1):
            specs.append(
                PageSpec(
                    f"menus-{group.menu_type.id}-{n}",
                    "game-day-menu.qmd.j2",
                    {
                        "type_title": group.menu_type.title,
                        "menus": [_menu_view(model, m) for m in chunk],
                    },
                    anchors=tuple(menu_label(m.id) for m in chunk),
                )
            )

    kinds = []
    for kind in model.settings.component_kinds:
        members = [c for c in model.components if c.kind.id == kind.id]
        if members:
            kinds.append(
                {
                    "title": kind.label,
                    "components": [
                        {
                            "ref": Ref(component_label(c.id), c.title),
                            "used_in": [r.title for r in model.usage[c.id].all],
                        }
                        for c in members
                    ],
                }
            )
    specs.append(
        PageSpec(
            "make-it-or-buy-it",
            "make-buy-index.qmd.j2",
            {"label": MAKE_BUY, "kinds": kinds},
            anchors=(MAKE_BUY,),
        )
    )
    for component in model.components:
        specs.append(component_page(model, component, media))

    return specs


def recipe_page(model: BookModel, recipe: Recipe, media: Media) -> PageSpec:
    return PageSpec(
        f"recipe-{recipe.id}",
        "recipe.qmd.j2",
        recipe_context(model, recipe, media),
        anchors=(recipe_label(recipe.id), recipe_end_label(recipe.id)),
        spans=((recipe_label(recipe.id), recipe_end_label(recipe.id)),),
    )


def component_page(model: BookModel, component: Component, media: Media) -> PageSpec:
    return PageSpec(
        f"component-{component.id}",
        "component.qmd.j2",
        component_context(model, component, media),
        anchors=(component_label(component.id),),
    )
