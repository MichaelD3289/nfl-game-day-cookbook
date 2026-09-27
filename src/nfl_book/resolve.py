"""Resolve validated content into the ordered model the renderer consumes.

This is where publication rules live: only published content, components
reachable from published recipes (or ``always_include``), book ordering.
Nothing here knows about page numbers; those come from LaTeX labels.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

from nfl_book.config import Settings
from nfl_book.indexes import IndexDefinition, IndexSection, build_index
from nfl_book.models.common import Status
from nfl_book.models.config import MenuType
from nfl_book.models.content import (
    Component,
    Content,
    CoverPage,
    DishOff,
    GameDayMenu,
    Recipe,
)
from nfl_book.models.nfl import Division, Team
from nfl_book.validation import component_graph, publication_roots

UNORDERED = 1_000_000


@dataclass(frozen=True)
class QuickOption:
    component: Component
    text: str


@dataclass(frozen=True)
class TeamSection:
    team: Team
    recipes: tuple[Recipe, ...]


@dataclass(frozen=True)
class DivisionSection:
    division: Division
    teams: tuple[TeamSection, ...]
    dishoffs: tuple[DishOff, ...]

    @property
    def recipes(self) -> tuple[Recipe, ...]:
        return tuple(r for t in self.teams for r in t.recipes)


@dataclass(frozen=True)
class ComponentUsage:
    direct: tuple[Recipe, ...]
    indirect: tuple[Recipe, ...]

    @property
    def all(self) -> tuple[Recipe, ...]:
        return self.direct + self.indirect


@dataclass(frozen=True)
class MenuGroup:
    menu_type: MenuType
    menus: tuple[GameDayMenu, ...]


@dataclass(frozen=True)
class ResolvedIndex:
    definition: IndexDefinition
    sections: tuple[IndexSection, ...]


@dataclass
class BookModel:
    settings: Settings
    cover: CoverPage | None
    divisions: list[DivisionSection]
    components: list[Component]
    menu_groups: list[MenuGroup]
    indexes: list[ResolvedIndex]
    usage: dict[str, ComponentUsage]
    quick_options: dict[str, list[QuickOption]]  # keyed by recipe id
    shortlinks: dict[str, str]
    recipes_by_id: dict[str, Recipe] = field(default_factory=dict)
    components_by_id: dict[str, Component] = field(default_factory=dict)
    division: Division | None = None

    @property
    def recipes(self) -> list[Recipe]:
        return [r for d in self.divisions for r in d.recipes]

    @property
    def menus(self) -> list[GameDayMenu]:
        return [m for g in self.menu_groups for m in g.menus]

    @property
    def dishoffs(self) -> list[DishOff]:
        return [d for s in self.divisions for d in s.dishoffs]


def _order_key(order: int | None, title: str, item_id: str) -> tuple[int, str, str]:
    return (UNORDERED if order is None else order, title.casefold(), item_id)


def recipe_sort_key(settings: Settings) -> Callable[[Recipe], tuple[int, int, int, str, str]]:
    team_order = settings.league.team_order()
    courses = [b.id for b in settings.course_index.buckets]

    def key(r: Recipe) -> tuple[int, int, int, str, str]:
        course = courses.index(r.meta.course) if r.meta.course in courses else len(courses)
        return (team_order[r.team.slug], course, *_order_key(r.meta.order, r.title, r.id))

    return key


def quick_options_for(
    item: Recipe | Component, components: dict[str, Component]
) -> list[QuickOption]:
    overrides = item.meta.quick_options if isinstance(item, Recipe) else {}
    options = []
    for ref in item.component_refs:
        component = components.get(ref)
        if component is not None:
            options.append(QuickOption(component, overrides.get(ref, component.meta.quick_buy)))
    return options


def resolve(
    settings: Settings,
    content: Content,
    shortlinks: dict[str, str],
    *,
    include: Callable[[Status], bool] = lambda s: s is Status.PUBLISHED,
    division: Division | None = None,
) -> BookModel:
    recipes = sorted(
        (
            r
            for r in content.recipes
            if include(r.meta.status) and (division is None or r.division.key == division.key)
        ),
        key=recipe_sort_key(settings),
    )
    all_components = {c.id: c for c in content.components}
    graph = component_graph(content.components)

    usage_direct: dict[str, list[Recipe]] = {}
    usage_indirect: dict[str, list[Recipe]] = {}
    for recipe in recipes:
        direct = set(recipe.component_refs)
        for cid in sorted(graph.closure(direct)):
            bucket = usage_direct if cid in direct else usage_indirect
            bucket.setdefault(cid, []).append(recipe)

    roots = (
        publication_roots(recipes, content.components, include)
        if division is None
        else {ref for recipe in recipes for ref in recipe.component_refs}
    )
    reachable = graph.closure(roots)
    kind_order = [k.id for k in settings.component_kinds]
    components = sorted(
        (c for c in content.components if include(c.meta.status) and c.id in reachable),
        key=lambda c: (kind_order.index(c.kind.id), *_order_key(c.meta.order, c.title, c.id)),
    )
    usage = {
        c.id: ComponentUsage(tuple(usage_direct.get(c.id, ())), tuple(usage_indirect.get(c.id, ())))
        for c in components
    }

    divisions = []
    selected_divisions = [division] if division is not None else settings.league.divisions
    for section_division in selected_divisions:
        teams = tuple(
            TeamSection(team, tuple(r for r in recipes if r.team.slug == team.slug))
            for team in section_division.teams
        )
        dishoffs = tuple(
            sorted(
                (
                    d
                    for d in content.dishoffs
                    if d.division.key == section_division.key and include(d.meta.status)
                ),
                key=lambda d: _order_key(d.meta.order, d.meta.title, d.id),
            )
        )
        divisions.append(DivisionSection(section_division, teams, dishoffs))

    recipe_ids = {r.id for r in recipes}
    menu_groups = []
    for menu_type in settings.menu_types:
        menus = sorted(
            (
                m
                for m in content.menus
                if m.menu_type.id == menu_type.id
                and include(m.meta.status)
                and (division is None or set(m.meta.recipes) <= recipe_ids)
            ),
            key=lambda m: _order_key(m.meta.order, m.meta.title, m.id),
        )
        if menus:
            menu_groups.append(MenuGroup(menu_type, tuple(menus)))

    indexes = []
    for config in settings.indexes:
        definition = build_index(config)
        indexes.append(ResolvedIndex(definition, tuple(definition.sections(recipes))))

    if division is not None:
        all_components = {c.id: c for c in components}

    return BookModel(
        settings=settings,
        cover=content.cover,
        divisions=divisions,
        components=components,
        menu_groups=menu_groups,
        indexes=indexes,
        usage=usage,
        quick_options={r.id: quick_options_for(r, all_components) for r in recipes},
        shortlinks=shortlinks,
        recipes_by_id={r.id: r for r in (content.recipes if division is None else recipes)},
        components_by_id=all_components,
        division=division,
    )


def menu_recipes(menu: GameDayMenu | DishOff, model: BookModel) -> Sequence[Recipe]:
    return [model.recipes_by_id[rid] for rid in menu.meta.recipes if rid in model.recipes_by_id]
