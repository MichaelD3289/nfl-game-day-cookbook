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
from nfl_book.models.content import Component, IngredientGroup, Recipe
from nfl_book.quantities import Amount
from nfl_book.references import (
    Address,
    IndexPage,
    Placed,
    SectionPage,
    address,
    component_label,
    edition_root,
    menu_label,
    menu_page_slug,
    recipe_label,
)
from nfl_book.resolve import BookModel, QuickOption, menu_recipes, quick_options_for

CONTENTS = address(SectionPage("contents"))
GAME_DAY = address(SectionPage("game-day-menus"))
MAKE_BUY = address(SectionPage("make-it-or-buy-it"))
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
    # Every anchor the page renders in the website and EPUB, as labels. Route tables are
    # built from this alone. End labels are the ends of ``spans``, not anchors.
    anchors: tuple[str, ...] = ()
    spans: tuple[tuple[str, str], ...] = ()  # (start label, end label) expected on one page


# --------------------------------------------------------------------------- views
@dataclass(frozen=True)
class Ref:
    label: str
    title: str
    note: str = ""
    # Recipe refs only: the parts of ``note``, kept apart so the website can style
    # them and leave out the team where the page is already about that team.
    team: str = ""
    course: str = ""


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


@dataclass(frozen=True)
class TimelineStepView:
    """One kickoff-timeline row: when, what, and the recipe it links to."""

    label: str
    task: str
    recipe: str  # "recipe:<id>" label, or "" for a general task
    minutes: int | None  # minutes from kickoff, only when the time maps to a clock


def _timeline(model: BookModel, menu: Any) -> list[TimelineStepView]:
    views = []
    for step in getattr(menu.meta, "timeline", None) or []:
        offset = step.offset
        recipe = recipe_label(step.recipe) if step.recipe in model.recipes_by_id else ""
        minutes = offset.minutes if offset.clock else None
        views.append(TimelineStepView(offset.label, step.task, recipe, minutes))
    return views


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


def _web(item: Recipe | Component, model: BookModel) -> WebView | None:
    """The item's page in this edition of the website; drafts have none."""
    href = address(item, website_url=model.settings.book.website_url).edition_url
    return None if href is None else WebView(href, __version__)


def _meta(*parts: tuple[str, str | None]) -> list[tuple[str, str]]:
    return [(name, value) for name, value in parts if value]


def _meta_line(*parts: tuple[str, str | None]) -> str:
    return "   |   ".join(f"{name}: {value}" for name, value in _meta(*parts))


def _course(model: BookModel, recipe: Recipe) -> str:
    bucket = model.settings.course(recipe.meta.course)
    return bucket.singular if bucket else recipe.meta.course


def _recipe_ref(model: BookModel, recipe: Recipe, *, course: bool = False) -> Ref:
    team = recipe.team.short_name
    kind = _course(model, recipe)
    note = f"{team}, {kind}" if course else team
    return Ref(recipe_label(recipe.id), recipe.title, note, team, kind)


# --------------------------------------------------------------------------- pages
def recipe_context(model: BookModel, recipe: Recipe, media: Media) -> dict[str, Any]:
    options = model.quick_options.get(recipe.id)
    if options is None:  # preview of unpublished content
        options = quick_options_for(recipe, model.components_by_id)
    where = address(recipe)
    return {
        "label": where.label,
        "end_label": where.end_label,
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
        "image": media.images.get(recipe_label(recipe.id), ""),
        "image_size": media.image_sizes.get(recipe_label(recipe.id), 0),
        "photo_credit": recipe.meta.photo_credit or "",
        "quick_options": _options(options),
        "groups": _groups(recipe.ingredients),
        "compact_ingredients": _compact(recipe.ingredients),
        "instructions": recipe.instructions,
        "kitchen_notes": recipe.kitchen_notes or "",
        "source": _source(recipe, model),
        "web": _web(recipe, model),
        "qr": media.qr.get(recipe_label(recipe.id), ""),
    }


def component_context(model: BookModel, component: Component, media: Media) -> dict[str, Any]:
    usage = model.usage.get(component.id)
    used_in = [_recipe_ref(model, r) for r in usage.all] if usage else []
    return {
        "label": component_label(component.id),
        "title": component.title,
        "description": component.meta.description or "",
        "kind": component.kind.singular,
        "meta_line": _meta_line(("Yield", component.meta.yield_)),
        "meta": _meta(("Yield", component.meta.yield_)),
        "groups": _groups(component.ingredients),
        "method": component.method,
        "note": component.note or "",
        "quick_buy": component.meta.quick_buy,
        "used_in": used_in,
        "source": _source(component, model),
        "web": _web(component, model),
        "qr": media.qr.get(component_label(component.id), ""),
    }


def _website(model: BookModel) -> dict[str, str] | None:
    base = model.settings.book.website_url
    if not base:
        return None
    href = edition_root(base)
    return {"href": href, "display": href.removeprefix("https://"), "edition": __version__}


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
        "timeline": _timeline(model, menu),
    }


def _span(where: Address) -> tuple[str, str]:
    """(start label, end label) of an item that must fit on one page."""
    assert where.end_label is not None, f"{where.label} has no end label"
    return where.label, where.end_label


def _chunks(items: Sequence[Any], size: int) -> list[Sequence[Any]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def build_pages(model: BookModel, media: Media) -> list[PageSpec]:
    """The whole book, in publication order."""
    specs: list[PageSpec] = []
    recipes = model.recipes

    cover = model.cover
    division = model.division
    cover_title = (cover.title if cover else "") or model.settings.book.title
    cover_subtitle = (cover.subtitle if cover else None) or model.settings.book.subtitle or ""
    cover_tagline = (cover.tagline if cover else None) or ""
    cover_body = cover.body if cover else ""
    if division is not None:
        cover_title = f"{model.settings.book.title}: {division.name}"
        cover_subtitle = f"{division.name} division booklet"
        cover_tagline = "Published recipes for your division's game day"
        cover_body = (
            f"{len(recipes)} recipes from {len({r.team.slug for r in recipes})} teams "
            f"in {division.name}.\n\n"
            "Includes the components these recipes use, division dish-offs, "
            "and game-day menus drawn entirely from this division."
        )
    specs.append(
        PageSpec(
            "cover",
            "cover.qmd.j2",
            {
                "title": cover_title,
                "subtitle": cover_subtitle,
                "tagline": cover_tagline,
                "body": cover_body,
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
            CONTENTS.slug,
            "contents.qmd.j2",
            {
                "label": CONTENTS.label,
                "indexes": [
                    Ref(address(IndexPage(i.definition.id)).label, i.definition.title)
                    for i in model.indexes
                ],
                "divisions": [
                    {
                        "ref": Ref(address(d.division).label, d.division.name),
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
                "game_day": Ref(GAME_DAY.label, "Game Day Menus"),
                "make_buy": Ref(MAKE_BUY.label, "Make It or Buy It"),
            },
            anchors=(CONTENTS.label,),
        )
    )

    for resolved in model.indexes:
        definition = resolved.definition
        where = address(IndexPage(definition.id))
        specs.append(
            PageSpec(
                where.slug,
                "index.qmd.j2",
                {
                    "label": where.label,
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
                anchors=(where.label,),
            )
        )

    for section in model.divisions:
        division = section.division
        where = address(division)
        team_addresses = {t.team.slug: address(Placed(t.team, where.slug)) for t in section.teams}
        # Teams without recipes are listed in print only: the website and EPUB skip them.
        anchored_teams = [team_addresses[t.team.slug] for t in section.teams if t.recipes]
        specs.append(
            PageSpec(
                where.slug,
                "division.qmd.j2",
                {
                    "label": where.label,
                    "end_label": where.end_label,
                    "name": division.name,
                    "conference": division.conference_name,
                    "teams": [
                        {
                            "label": team_addresses[t.team.slug].label,
                            "name": t.team.name,
                            "location": t.team.location,
                            "recipes": [_recipe_ref(model, r, course=True) for r in t.recipes],
                        }
                        for t in section.teams
                    ],
                    "dishoffs": [_menu_view(model, d) for d in section.dishoffs],
                },
                anchors=(
                    where.label,
                    *(a.label for a in anchored_teams),
                    *(address(d).label for d in section.dishoffs),
                ),
                spans=(_span(where),),
            )
        )
        for recipe in section.recipes:
            specs.append(recipe_page(model, recipe, media))

    specs.append(
        PageSpec(
            GAME_DAY.slug,
            "game-day-index.qmd.j2",
            {
                "label": GAME_DAY.label,
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
            anchors=(GAME_DAY.label,),
        )
    )
    for group in model.menu_groups:
        for n, chunk in enumerate(_chunks(group.menus, MENUS_PER_PAGE), start=1):
            slug = menu_page_slug(group.menu_type.id, n)
            placed = [address(Placed(m, slug)) for m in chunk]
            end = placed[-1].end_label
            assert end is not None
            specs.append(
                PageSpec(
                    slug,
                    "game-day-menu.qmd.j2",
                    {
                        "type_title": group.menu_type.title,
                        "end_label": end,
                        "menus": [_menu_view(model, m) for m in chunk],
                    },
                    anchors=tuple(a.label for a in placed),
                    spans=((placed[0].label, end),),
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
                            "used_in_refs": [_recipe_ref(model, r) for r in model.usage[c.id].all],
                        }
                        for c in members
                    ],
                }
            )
    specs.append(
        PageSpec(
            MAKE_BUY.slug,
            "make-buy-index.qmd.j2",
            {"label": MAKE_BUY.label, "kinds": kinds},
            anchors=(MAKE_BUY.label,),
        )
    )
    for component in model.components:
        specs.append(component_page(model, component, media))

    return specs


def recipe_page(model: BookModel, recipe: Recipe, media: Media) -> PageSpec:
    where = address(recipe)
    return PageSpec(
        where.slug,
        "recipe.qmd.j2",
        recipe_context(model, recipe, media),
        anchors=(where.label,),
        spans=(_span(where),),
    )


def component_page(model: BookModel, component: Component, media: Media) -> PageSpec:
    where = address(component)
    return PageSpec(
        where.slug,
        "component.qmd.j2",
        component_context(model, component, media),
        anchors=(where.label,),
    )
