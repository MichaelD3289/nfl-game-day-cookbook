"""The website's page views and the builders that compute each field once.

The website extends the base views of ``nfl_book.render.views`` with scaling, JSON-LD,
print pages and suggestions. Every builder takes the item a page is about, so no field
is recovered afterwards by comparing template names or parsing labels, and nothing edits
a page once it is built. The catalog is built first, from the model, and the pages that
list recipes (Browse, Build your own menu, Matchup) read from it.
"""

from __future__ import annotations

import html
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode

from nfl_book.catalog import Catalog, CatalogFacet, CatalogRecipe
from nfl_book.models.content import Component, DishOff, GameDayMenu, Recipe
from nfl_book.payloads import attribute_json, script_json
from nfl_book.publishing import REPOSITORY
from nfl_book.quantities import Amount, find_yield_amounts
from nfl_book.references import SectionPage, address
from nfl_book.render.pages import (
    CONTENTS,
    GAME_DAY,
    MAKE_BUY,
    Media,
    PageBuilders,
    PageSpec,
    component_spec,
    component_view,
    division_spec,
    division_view,
    game_day_index_view,
    make_buy_view,
    menu_page_view,
    menu_pages,
    menu_view,
    recipe_spec,
    recipe_view,
)
from nfl_book.render.views import (
    ComponentView,
    DivisionView,
    GameDayIndexView,
    MakeBuyView,
    MenuPageView,
    MenuView,
    PageView,
    RecipeView,
    TeamView,
    view_fields,
)
from nfl_book.resolve import BookModel, DivisionSection, MenuGroup, menu_recipes
from nfl_book.structured_data import head_html, recipe_json_ld

# Quick issue form per suggestion kind: (template, title prefix, field used in the title).
SUGGESTION_FORMS = {
    "edit": ("suggest-edit.yml", "Edit suggestion: ", "item"),
    "recipe": ("quick-recipe.yml", "Recipe idea: ", "dish"),
    "component": ("quick-component.yml", "Component idea: ", "name"),
    "menu": ("quick-menu.yml", "Menu idea: ", ""),
    "dish-off": ("quick-dish-off.yml", "Dish-off idea: ", ""),
}

# Recipe multipliers offered on scalable pages: (label, factor as "n" or "n/d").
MULTIPLIERS = (("½×", "1/2"), ("1×", "1"), ("1½×", "3/2"), ("2×", "2"), ("3×", "3"), ("4×", "4"))


# --------------------------------------------------------------------------- parts
@dataclass(frozen=True)
class Suggestion:
    """A prefilled GitHub issue link plus the same fields for the anonymous form."""

    kind: str
    lead: str
    github: str
    fields: str  # JSON


@dataclass(frozen=True)
class Scaler:
    multipliers: tuple[tuple[str, str], ...]
    servings: int | None
    servings_max: int | None
    serves: str


def suggestion(kind: str, lead: str, **fields: str) -> Suggestion:
    template, prefix, title_field = SUGGESTION_FORMS[kind]
    query = {"template": template, "title": prefix + fields.get(title_field, "")}
    query.update({k: v for k, v in fields.items() if v})
    return Suggestion(
        kind,
        lead,
        f"{REPOSITORY}/issues/new?{urlencode(query)}",
        attribute_json(fields),
    )


def marked(text: str, amounts: Iterable[Amount], plain: Callable[[str], str] = str) -> str:
    """``text`` with each scalable amount wrapped for website-scale.js; ``plain`` escapes
    the text between them."""
    parts = []
    position = 0
    for amount in amounts:
        attrs = {"data-q": str(amount.low)}
        if amount.high is not None:
            attrs["data-q2"] = str(amount.high)
        if amount.unit:
            attrs["data-unit"] = amount.unit
        if amount.adjective:
            attrs["data-adj"] = amount.adjective
        shown = " ".join(f'{k}="{html.escape(v)}"' for k, v in attrs.items())
        parts.append(plain(text[position : amount.start]))
        parts.append(f'<span class="qty" {shown}>{plain(text[amount.start : amount.end])}</span>')
        position = amount.end
    parts.append(plain(text[position:]))
    return "".join(parts)


@dataclass(frozen=True)
class _Scaling:
    scaler: Scaler | None
    yield_html: str
    yield_fixed: bool


def _scaling(
    view: RecipeView | ComponentView, yield_text: str | None, servings: tuple[int, int] | None
) -> _Scaling:
    """Scaling controls for a page that has amounts to scale; the yield grows with the
    batch too, and one it cannot scale says how many batches."""
    if not any(item.amounts for group in view.groups for item in group.items):
        return _Scaling(None, "", False)
    yield_html, yield_fixed = "", False
    if yield_text:
        amounts = find_yield_amounts(yield_text)
        yield_html = marked(yield_text, amounts, html.escape)
        yield_fixed = not amounts
    low = high = None
    serves = ""
    if servings:
        low, high = servings
        serves = str(low) if low == high else f"{low}–{high}"
    return _Scaling(Scaler(MULTIPLIERS, low, high, serves), yield_html, yield_fixed)


def _source_path(path: Path, model: BookModel) -> str:
    root = model.content_root
    return (path.relative_to(root) if root else path).as_posix()


def recipe_print_pages(recipe: Recipe, model: BookModel) -> tuple[str, ...]:
    """The component pages print.js prints after ``recipe``: every component it uses,
    nested ones included, once each in order of first appearance."""
    return tuple(address(c).page_url for c in model.components_for(recipe))


# ------------------------------------------------------------------------- recipes
@dataclass(frozen=True)
class WebRecipeView(RecipeView):
    scaler: Scaler | None
    yield_html: str
    yield_fixed: bool
    head: str  # schema.org JSON-LD and the canonical address, for the page head
    print_pages: tuple[str, ...]
    suggest: Suggestion


@dataclass(frozen=True)
class WebComponentView(ComponentView):
    scaler: Scaler | None
    yield_html: str
    yield_fixed: bool
    suggest: Suggestion


def recipe_page(recipe: Recipe, model: BookModel, media: Media, catalog: Catalog) -> PageSpec:
    """The website page of ``recipe``. ``catalog`` is the site's recipe catalog; a recipe
    page needs nothing from it yet."""
    base = recipe_view(model, recipe, media)
    where = address(recipe)
    site = model.settings.book.website_url
    edition = model.settings.edition_root
    # The canonical address is the page at the website root, which always serves the
    # latest edition; ``url`` and ``image`` name this edition's own copies.
    image_url = f"{edition}{base.image}" if edition and base.image else None
    canonical = f"{site.rstrip('/')}/{where.page_url}" if site else None
    data = recipe_json_ld(
        recipe,
        model.settings,
        image_url=image_url,
        page_url=base.web.href if base.web else None,
    )
    scaling = _scaling(base, recipe.meta.yield_, recipe.servings)
    view = WebRecipeView(
        **view_fields(base),
        scaler=scaling.scaler,
        yield_html=scaling.yield_html,
        yield_fixed=scaling.yield_fixed,
        head=head_html(data, canonical),
        print_pages=recipe_print_pages(recipe, model),
        suggest=suggestion(
            "edit",
            "Spot something to fix in this recipe?",
            item=f"{recipe.title} ({recipe.team.name}) [{base.label}]",
            page=_source_path(recipe.path, model),
        ),
    )
    return recipe_spec(recipe, view)


def component_page(
    component: Component, model: BookModel, media: Media, catalog: Catalog
) -> PageSpec:
    """The website page of ``component``."""
    base = component_view(model, component, media)
    scaling = _scaling(base, component.meta.yield_, None)
    view = WebComponentView(
        **view_fields(base),
        scaler=scaling.scaler,
        yield_html=scaling.yield_html,
        yield_fixed=scaling.yield_fixed,
        suggest=suggestion(
            "edit",
            "Spot something to fix in this component?",
            item=f"{component.title} [{base.label}]",
            page=_source_path(component.path, model),
        ),
    )
    return component_spec(component, view)


# ---------------------------------------------------------------- menus & divisions
@dataclass(frozen=True)
class WebMenuView(MenuView):
    """A menu or dish-off card with the pages print.js prints for it."""

    print_pages: tuple[str, ...]
    print_components: tuple[str, ...]  # every component those recipes print, once each


@dataclass(frozen=True)
class WebMenuPageView(MenuPageView):
    menus: tuple[WebMenuView, ...]


@dataclass(frozen=True)
class WebTeamView(TeamView):
    suggest: Suggestion


@dataclass(frozen=True)
class WebDivisionView(DivisionView):
    teams: tuple[WebTeamView, ...]
    dishoffs: tuple[WebMenuView, ...]
    suggest: Suggestion
    suggest_dishoff: Suggestion


def web_menu_view(menu: GameDayMenu | DishOff, model: BookModel) -> WebMenuView:
    """A menu card prints its recipes in menu order, then optionally every component
    those recipes print, once each."""
    recipes = menu_recipes(menu, model)
    components = dict.fromkeys(url for r in recipes for url in recipe_print_pages(r, model))
    return WebMenuView(
        **view_fields(menu_view(model, menu)),
        print_pages=tuple(address(r).page_url for r in recipes),
        print_components=tuple(components),
    )


def division_page(section: DivisionSection, model: BookModel) -> PageSpec:
    base = division_view(model, section)
    name = base.name
    fields = view_fields(base)
    fields.update(
        teams=tuple(
            WebTeamView(
                **view_fields(team),
                suggest=suggestion(
                    "recipe",
                    f"Know another {team.name} dish?",
                    team=f"{team.name} ({team.location})",
                ),
            )
            for team in base.teams
        ),
        dishoffs=tuple(web_menu_view(d, model) for d in section.dishoffs),
        suggest=suggestion("recipe", f"Missing a dish from a {name} team?", team=""),
        suggest_dishoff=suggestion(
            "dish-off", f"Have an idea for a {name} dish-off?", division=name
        ),
    )
    return division_spec(section, WebDivisionView(**fields))


def menu_pages_for(group: MenuGroup, model: BookModel) -> list[PageSpec]:
    def build(g: MenuGroup, chunk: Sequence[GameDayMenu], end: str) -> PageView:
        fields = view_fields(menu_page_view(model, g, chunk, end))
        fields.update(menus=tuple(web_menu_view(m, model) for m in chunk))
        return WebMenuPageView(**fields)

    return menu_pages(group, build)


# ------------------------------------------------------------------ section indexes
@dataclass(frozen=True)
class WebGameDayIndexView(GameDayIndexView):
    suggest: Suggestion


@dataclass(frozen=True)
class WebMakeBuyView(MakeBuyView):
    suggest: Suggestion


def game_day_index_page(model: BookModel) -> PageSpec:
    view = WebGameDayIndexView(
        **view_fields(game_day_index_view(model)),
        suggest=suggestion("menu", "Have an idea for a game-day menu?"),
    )
    return PageSpec(GAME_DAY.slug, "game-day-index.qmd.j2", view, anchors=(GAME_DAY.label,))


def make_buy_page(model: BookModel) -> PageSpec:
    view = WebMakeBuyView(
        **view_fields(make_buy_view(model)),
        suggest=suggestion("component", "Know a sauce, dip, or side we should add?"),
    )
    return PageSpec(MAKE_BUY.slug, "make-buy-index.qmd.j2", view, anchors=(MAKE_BUY.label,))


# ------------------------------------------------------------- catalog-driven pages
@dataclass(frozen=True)
class BrowseView(PageView):
    title: str
    label: str
    facets: tuple[CatalogFacet, ...]
    recipes: tuple[CatalogRecipe, ...]

    @property
    def page_title(self) -> str:
        return self.title


@dataclass(frozen=True)
class RecipeCard(CatalogRecipe):
    """A catalog recipe with the cooking-time label the home page and menus show."""

    time_label: str


@dataclass(frozen=True)
class MenuDish(CatalogRecipe):
    """A catalog recipe as the menu builder lists it."""

    print_pages: tuple[str, ...]


@dataclass(frozen=True)
class MenuCourse:
    id: str
    label: str
    dishes: tuple[MenuDish, ...]


@dataclass(frozen=True)
class MenuBuilderView(PageView):
    title: str
    label: str
    facets: tuple[CatalogFacet, ...]
    courses: tuple[MenuCourse, ...]
    total: int
    multipliers: tuple[tuple[str, str], ...]
    suggest: Suggestion

    @property
    def page_title(self) -> str:
        return self.title


@dataclass(frozen=True)
class PickerTeam:
    slug: str
    name: str
    empty: bool


@dataclass(frozen=True)
class Picker:
    label: str
    teams: tuple[PickerTeam, ...]


@dataclass(frozen=True)
class MatchupCourse:
    id: str
    label: str
    singular: str


@dataclass(frozen=True)
class MatchupDivision:
    key: str
    name: str


@dataclass(frozen=True)
class MatchupTeam:
    slug: str
    name: str
    short: str
    division: str


@dataclass(frozen=True)
class MatchupDish:
    id: str
    title: str
    url: str
    course: str
    team: str
    division: str
    print_pages: tuple[str, ...]


@dataclass(frozen=True)
class MatchupData:
    """The matchup page's embedded payload, read by ``readData`` in website-matchup.js."""

    courses: tuple[MatchupCourse, ...]
    divisions: tuple[MatchupDivision, ...]
    teams: tuple[MatchupTeam, ...]
    dishes: tuple[MatchupDish, ...]


@dataclass(frozen=True)
class MatchupView(PageView):
    title: str
    label: str
    pickers: tuple[Picker, ...]
    data_json: str
    suggest: Suggestion

    @property
    def page_title(self) -> str:
        return self.title


def browse_page(model: BookModel, catalog: Catalog) -> PageSpec:
    """The Browse recipes page, right after All recipes."""
    where = address(SectionPage("browse"))
    view = BrowseView("Browse recipes", where.label, catalog.facets, catalog.recipes)
    return PageSpec(where.slug, "browse.qmd.j2", view, anchors=(where.label,))


def menu_builder_page(model: BookModel, catalog: Catalog) -> PageSpec:
    """The Build your own menu page, right after Game Day Menus.

    Dishes are grouped by course in data/indexes.yml order, empty courses left out, and
    keep book order within a course. Each carries the component pages its recipe prints.
    """
    courses = []
    for option in catalog.facet("course").options:
        dishes = tuple(
            MenuDish(
                **view_fields(entry),
                print_pages=recipe_print_pages(model.recipes_by_id[entry.id], model),
            )
            for entry in catalog.recipes
            if entry.course == option.id
        )
        if dishes:
            courses.append(MenuCourse(option.id, option.label, dishes))
    where = address(SectionPage("menu-builder"))
    view = MenuBuilderView(
        title="Build your own menu",
        label=where.label,
        facets=catalog.facets,
        courses=tuple(courses),
        total=sum(len(c.dishes) for c in courses),
        multipliers=MULTIPLIERS,
        # menu.js fills the idea field with the picked dishes and the menu address.
        suggest=suggestion("menu", "Think your menu belongs in the book?"),
    )
    return PageSpec(where.slug, "menu-builder.qmd.j2", view, anchors=(where.label,))


def matchup_page(model: BookModel, catalog: Catalog) -> PageSpec:
    """The Matchup menu page, right after Build your own menu.

    Embeds every team grouped by division, and every published dish with its course,
    team, division and the component pages it prints, for matchup.js to pick from.
    Courses with no dishes are left out; the rest keep data/indexes.yml order.
    """
    present = {recipe.course for recipe in catalog.recipes}
    courses = []
    for option in catalog.facet("course").options:
        if option.id in present:
            bucket = model.settings.course(option.id)
            singular = bucket.singular if bucket else option.label
            courses.append(MatchupCourse(option.id, option.label, singular))
    dishes = tuple(
        MatchupDish(
            id=recipe.id,
            title=recipe.title,
            url=recipe.url,
            course=recipe.course,
            team=recipe.team.slug,
            division=recipe.division,
            print_pages=recipe_print_pages(model.recipes_by_id[recipe.id], model),
        )
        for recipe in catalog.recipes
    )
    with_dishes = {dish.team for dish in dishes}
    pickers = tuple(
        Picker(
            section.division.name,
            tuple(
                PickerTeam(entry.team.slug, entry.team.name, entry.team.slug not in with_dishes)
                for entry in section.teams
            ),
        )
        for section in model.divisions
    )
    data = MatchupData(
        courses=tuple(courses),
        divisions=tuple(
            MatchupDivision(section.division.key, section.division.name)
            for section in model.divisions
        ),
        teams=tuple(
            MatchupTeam(
                entry.team.slug, entry.team.name, entry.team.short_name, section.division.key
            )
            for section in model.divisions
            for entry in section.teams
        ),
        dishes=dishes,
    )
    where = address(SectionPage("matchup"))
    view = MatchupView(
        title="Matchup menu",
        label=where.label,
        pickers=pickers,
        data_json=script_json(data),
        suggest=suggestion("menu", "Have an idea for a game-day menu?"),
    )
    return PageSpec(where.slug, "matchup.qmd.j2", view, anchors=(where.label,))


# ------------------------------------------------------------------------ the site
def site_builders(model: BookModel, media: Media, catalog: Catalog) -> PageBuilders:
    """Page builders for the website: the base views, extended."""
    return PageBuilders(
        recipe=lambda recipe: recipe_page(recipe, model, media, catalog),
        component=lambda component: component_page(component, model, media, catalog),
        division=lambda section: division_page(section, model),
        menus=lambda group: menu_pages_for(group, model),
        game_day_index=lambda: game_day_index_page(model),
        make_buy=lambda: make_buy_page(model),
        after={
            CONTENTS.slug: [browse_page(model, catalog)],
            GAME_DAY.slug: [menu_builder_page(model, catalog), matchup_page(model, catalog)],
        },
    )
