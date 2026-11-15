"""Turn the resolved :class:`BookModel` into an ordered list of page specs.

Each :class:`PageSpec` names a Jinja template, the typed page view it renders
(:mod:`nfl_book.render.views`) and the LaTeX labels it is expected to anchor. Views hold
labels, never page numbers: every number in the book is resolved by LaTeX from those
labels.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from nfl_book.models.content import Component, DishOff, GameDayMenu, IngredientGroup, Recipe
from nfl_book.references import (
    Address,
    IndexPage,
    Placed,
    SectionPage,
    address,
    component_label,
    menu_label,
    menu_page_slug,
    recipe_label,
)
from nfl_book.render.views import (
    BookStats,
    ComponentView,
    ContentsDivision,
    ContentsTeam,
    ContentsView,
    CoverView,
    DivisionView,
    GameDayIndexView,
    GroupView,
    IndexSectionView,
    IndexView,
    ItemView,
    MakeBuyComponent,
    MakeBuyKind,
    MakeBuyView,
    MenuGroupView,
    MenuPageView,
    MenuView,
    OptionView,
    PageView,
    RecipeView,
    Ref,
    SourceView,
    TeamView,
    TimelineStepView,
    WebsiteLink,
    WebView,
)
from nfl_book.resolve import (
    BookModel,
    DivisionSection,
    MenuGroup,
    QuickOption,
    menu_recipes,
    quick_options_for,
)

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
    view: PageView
    # Every anchor the page renders in the website and EPUB, as labels. Route tables are
    # built from this alone. End labels are the ends of ``spans``, not anchors.
    anchors: tuple[str, ...] = ()
    spans: tuple[tuple[str, str], ...] = ()  # (start label, end label) expected on one page


EXAMPLE_UNUSED = None

# Past this many ingredient lines a bulleted list cannot share a page with the
# instructions, so groups are set as run-in paragraphs (as in the print booklet).
COMPACT_INGREDIENTS_OVER = 24


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


def _groups(groups: Iterable[IngredientGroup]) -> tuple[GroupView, ...]:
    return tuple(
        GroupView(
            g.heading,
            tuple(
                ItemView(i.text, component_label(i.component) if i.component else None, i.amounts)
                for i in g.items
            ),
        )
        for g in groups
    )


def _options(options: Sequence[QuickOption]) -> tuple[OptionView, ...]:
    return tuple(
        OptionView(component_label(o.component.id), o.component.title, o.text) for o in options
    )


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
    href = address(item, edition=model.settings.edition_root).edition_url
    return None if href is None else WebView(href, model.settings.version)


def _meta(*parts: tuple[str, str | None]) -> tuple[tuple[str, str], ...]:
    return tuple((name, value) for name, value in parts if value)


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


# ---------------------------------------------------------------------------- views
def recipe_view(model: BookModel, recipe: Recipe, media: Media) -> RecipeView:
    """The base view of a recipe, shared by every format."""
    options = model.quick_options.get(recipe.id)
    if options is None:  # preview of unpublished content
        options = quick_options_for(recipe, model.components_by_id)
    where = address(recipe)
    facts = (
        ("Yield", recipe.meta.yield_),
        ("Prep", recipe.meta.prep),
        ("Cook", recipe.meta.cook),
    )
    return RecipeView(
        label=where.label,
        end_label=where.end_label,
        title=recipe.title,
        team=recipe.team.name,
        location=recipe.location,
        course=_course(model, recipe),
        division=recipe.division.name,
        meta_line=_meta_line(*facts),
        meta=_meta(*facts),
        description=recipe.meta.description or "",
        image=media.images.get(recipe_label(recipe.id), ""),
        image_size=media.image_sizes.get(recipe_label(recipe.id), 0),
        photo_credit=recipe.meta.photo_credit or "",
        quick_options=_options(options),
        groups=_groups(recipe.ingredients),
        compact_ingredients=_compact(recipe.ingredients),
        instructions=recipe.instructions,
        kitchen_notes=recipe.kitchen_notes or "",
        source=_source(recipe, model),
        web=_web(recipe, model),
        qr=media.qr.get(recipe_label(recipe.id), ""),
    )


def component_view(model: BookModel, component: Component, media: Media) -> ComponentView:
    """The base view of a component, shared by every format."""
    usage = model.usage.get(component.id)
    used_in = tuple(_recipe_ref(model, r) for r in usage.all) if usage else ()
    return ComponentView(
        label=component_label(component.id),
        title=component.title,
        description=component.meta.description or "",
        kind=component.kind.singular,
        kind_id=component.kind.id,
        meta_line=_meta_line(("Yield", component.meta.yield_)),
        meta=_meta(("Yield", component.meta.yield_)),
        groups=_groups(component.ingredients),
        method=component.method,
        note=component.note or "",
        quick_buy=component.meta.quick_buy,
        used_in=used_in,
        source=_source(component, model),
        web=_web(component, model),
        qr=media.qr.get(component_label(component.id), ""),
    )


def menu_view(model: BookModel, menu: GameDayMenu | DishOff) -> MenuView:
    return MenuView(
        label=menu_label(menu.id),
        title=menu.meta.title,
        subtitle=getattr(menu.meta, "subtitle", None) or "",
        recipes=tuple(_recipe_ref(model, r, course=True) for r in menu_recipes(menu, model)),
        why_it_works=getattr(menu.meta, "why_it_works", None) or "",
        prep_plan=getattr(menu.meta, "prep_plan", None) or "",
        description=getattr(menu.meta, "description", None) or "",
        prep_note=getattr(menu.meta, "prep_note", None) or "",
        timeline=tuple(_timeline(model, menu)),
    )


def _website(model: BookModel) -> WebsiteLink | None:
    href = model.settings.edition_root
    if not href:
        return None
    return WebsiteLink(href, href.removeprefix("https://"), model.settings.version)


def _span(where: Address) -> tuple[str, str]:
    """(start label, end label) of an item that must fit on one page."""
    assert where.end_label is not None, f"{where.label} has no end label"
    return where.label, where.end_label


def _chunks(items: Sequence[Any], size: int) -> list[Sequence[Any]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


# ---------------------------------------------------------------------------- pages
def recipe_spec(recipe: Recipe, view: RecipeView, template: str = "recipe.qmd.j2") -> PageSpec:
    where = address(recipe)
    return PageSpec(where.slug, template, view, anchors=(where.label,), spans=(_span(where),))


def component_spec(
    component: Component, view: ComponentView, template: str = "component.qmd.j2"
) -> PageSpec:
    where = address(component)
    return PageSpec(where.slug, template, view, anchors=(where.label,))


def recipe_page(model: BookModel, recipe: Recipe, media: Media) -> PageSpec:
    return recipe_spec(recipe, recipe_view(model, recipe, media))


def component_page(model: BookModel, component: Component, media: Media) -> PageSpec:
    return component_spec(component, component_view(model, component, media))


def division_view(model: BookModel, section: DivisionSection) -> DivisionView:
    division = section.division
    where = address(division)
    team_addresses = {t.team.slug: address(Placed(t.team, where.slug)) for t in section.teams}
    return DivisionView(
        label=where.label,
        end_label=where.end_label,
        name=division.name,
        conference=division.conference_name,
        teams=tuple(
            TeamView(
                team_addresses[t.team.slug].label,
                t.team.name,
                t.team.location,
                tuple(_recipe_ref(model, r, course=True) for r in t.recipes),
            )
            for t in section.teams
        ),
        dishoffs=tuple(menu_view(model, d) for d in section.dishoffs),
    )


def division_spec(section: DivisionSection, view: DivisionView) -> PageSpec:
    where = address(section.division)
    team_addresses = {t.team.slug: address(Placed(t.team, where.slug)) for t in section.teams}
    # Teams without recipes are listed in print only: the website and EPUB skip them.
    anchored_teams = [team_addresses[t.team.slug] for t in section.teams if t.recipes]
    return PageSpec(
        where.slug,
        "division.qmd.j2",
        view,
        anchors=(
            where.label,
            *(a.label for a in anchored_teams),
            *(address(d).label for d in section.dishoffs),
        ),
        spans=(_span(where),),
    )


def division_page(model: BookModel, section: DivisionSection) -> PageSpec:
    return division_spec(section, division_view(model, section))


def menu_page_view(
    model: BookModel, group: MenuGroup, menus: Sequence[GameDayMenu], end: str
) -> MenuPageView:
    return MenuPageView(
        type_title=group.menu_type.title,
        end_label=end,
        menus=tuple(menu_view(model, m) for m in menus),
    )


def menu_pages(
    group: MenuGroup, build: Callable[[MenuGroup, Sequence[GameDayMenu], str], PageView]
) -> list[PageSpec]:
    """The pages of one menu type, each holding up to ``MENUS_PER_PAGE`` menus."""
    specs = []
    for n, chunk in enumerate(_chunks(group.menus, MENUS_PER_PAGE), start=1):
        slug = menu_page_slug(group.menu_type.id, n)
        placed = [address(Placed(m, slug)) for m in chunk]
        end = placed[-1].end_label
        assert end is not None
        specs.append(
            PageSpec(
                slug,
                "game-day-menu.qmd.j2",
                build(group, chunk, end),
                anchors=tuple(a.label for a in placed),
                spans=((placed[0].label, end),),
            )
        )
    return specs


def game_day_index_view(model: BookModel) -> GameDayIndexView:
    return GameDayIndexView(
        label=GAME_DAY.label,
        groups=tuple(
            MenuGroupView(
                g.menu_type.title,
                g.menu_type.description or "",
                tuple(Ref(menu_label(m.id), m.meta.title, m.meta.subtitle or "") for m in g.menus),
            )
            for g in model.menu_groups
        ),
    )


def game_day_index_page(model: BookModel) -> PageSpec:
    return PageSpec(
        GAME_DAY.slug,
        "game-day-index.qmd.j2",
        game_day_index_view(model),
        anchors=(GAME_DAY.label,),
    )


def make_buy_view(model: BookModel) -> MakeBuyView:
    kinds = []
    for kind in model.settings.component_kinds:
        members = [c for c in model.components if c.kind.id == kind.id]
        if members:
            kinds.append(
                MakeBuyKind(
                    kind.label,
                    tuple(
                        MakeBuyComponent(
                            Ref(component_label(c.id), c.title),
                            tuple(r.title for r in model.usage[c.id].all),
                            tuple(_recipe_ref(model, r) for r in model.usage[c.id].all),
                        )
                        for c in members
                    ),
                )
            )
    return MakeBuyView(MAKE_BUY.label, tuple(kinds))


def make_buy_page(model: BookModel) -> PageSpec:
    return PageSpec(
        MAKE_BUY.slug, "make-buy-index.qmd.j2", make_buy_view(model), anchors=(MAKE_BUY.label,)
    )


@dataclass(frozen=True)
class PageBuilders:
    """How each page kind is built for one format. ``after`` lists pages to place right
    after the page with the given slug (the website's own pages)."""

    recipe: Callable[[Recipe], PageSpec]
    component: Callable[[Component], PageSpec]
    division: Callable[[DivisionSection], PageSpec]
    menus: Callable[[MenuGroup], list[PageSpec]]
    game_day_index: Callable[[], PageSpec]
    make_buy: Callable[[], PageSpec]
    after: Mapping[str, Sequence[PageSpec]] = field(default_factory=dict)


def print_builders(model: BookModel, media: Media) -> PageBuilders:
    """The base views, which the print book, EPUB and (extended) the website share."""
    return PageBuilders(
        recipe=lambda recipe: recipe_page(model, recipe, media),
        component=lambda component: component_page(model, component, media),
        division=lambda section: division_page(model, section),
        menus=lambda group: menu_pages(
            group, lambda g, chunk, end: menu_page_view(model, g, chunk, end)
        ),
        game_day_index=lambda: game_day_index_page(model),
        make_buy=lambda: make_buy_page(model),
    )


def _cover_view(model: BookModel) -> CoverView:
    recipes = model.recipes
    cover = model.cover
    division = model.division
    title = (cover.title if cover else "") or model.settings.book.title
    subtitle = (cover.subtitle if cover else None) or model.settings.book.subtitle or ""
    tagline = (cover.tagline if cover else None) or ""
    body = cover.body if cover else ""
    if division is not None:
        title = f"{model.settings.book.title}: {division.name}"
        subtitle = f"{division.name} division booklet"
        tagline = "Published recipes for your division's game day"
        body = (
            f"{len(recipes)} recipes from {len({r.team.slug for r in recipes})} teams "
            f"in {division.name}.\n\n"
            "Includes the components these recipes use, division dish-offs, "
            "and game-day menus drawn entirely from this division."
        )
    return CoverView(
        title=title,
        subtitle=subtitle,
        tagline=tagline,
        body=body,
        website=_website(model),
        stats=BookStats(
            recipes=len(recipes),
            teams=len({r.team.slug for r in recipes}),
            components=len(model.components),
            menus=len(model.menus),
        ),
    )


def _contents_view(model: BookModel) -> ContentsView:
    return ContentsView(
        label=CONTENTS.label,
        indexes=tuple(
            Ref(address(IndexPage(i.definition.id)).label, i.definition.title)
            for i in model.indexes
        ),
        divisions=tuple(
            ContentsDivision(
                Ref(address(d.division).label, d.division.name),
                tuple(
                    ContentsTeam(t.team.name, tuple(_recipe_ref(model, r) for r in t.recipes))
                    for t in d.teams
                    if t.recipes
                ),
            )
            for d in model.divisions
        ),
        game_day=Ref(GAME_DAY.label, "Game Day Menus"),
        make_buy=Ref(MAKE_BUY.label, "Make It or Buy It"),
    )


def build_pages(
    model: BookModel, media: Media, builders: PageBuilders | None = None
) -> list[PageSpec]:
    """The whole book, in publication order."""
    build = builders or print_builders(model, media)
    specs: list[PageSpec] = []

    def add(spec: PageSpec) -> None:
        specs.append(spec)
        specs.extend(build.after.get(spec.slug, ()))

    add(PageSpec("cover", "cover.qmd.j2", _cover_view(model)))
    add(
        PageSpec(CONTENTS.slug, "contents.qmd.j2", _contents_view(model), anchors=(CONTENTS.label,))
    )
    for resolved in model.indexes:
        definition = resolved.definition
        where = address(IndexPage(definition.id))
        view = IndexView(
            label=where.label,
            title=definition.title,
            intro=definition.config.intro or "",
            sections=tuple(
                IndexSectionView(s.bucket.label, tuple(_recipe_ref(model, r) for r in s.recipes))
                for s in resolved.sections
            ),
        )
        add(PageSpec(where.slug, "index.qmd.j2", view, anchors=(where.label,)))
    for section in model.divisions:
        add(build.division(section))
        for recipe in section.recipes:
            add(build.recipe(recipe))
    add(build.game_day_index())
    for group in model.menu_groups:
        for spec in build.menus(group):
            add(spec)
    add(build.make_buy())
    for component in model.components:
        add(build.component(component))
    return specs
