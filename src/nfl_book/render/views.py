"""Page views: the data one page shows, prepared once for a given output format.

Every view is a frozen dataclass. A recipe and a component have one base view that
serves every format; the website extends it (``nfl_book.website_pages``) and the cards
extend it too. Views hold labels, never page numbers: LaTeX resolves those.

Templates read a view's fields as top-level variables, so ``{{ title }}`` and
``{{ item.text }}`` work the same on a view as they did on a dict.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields
from typing import Any

from nfl_book.quantities import Amount


class PageView:
    """Base of every page view."""

    @property
    def page_title(self) -> str:
        """The page's title, for the window title of formats that have one."""
        raise NotImplementedError


def view_fields(view: object) -> dict[str, Any]:
    """The fields of ``view`` by name, one level deep (nested views stay views)."""
    return {f.name: getattr(view, f.name) for f in fields(view)}  # type: ignore[arg-type]


# ----------------------------------------------------------------------- shared parts
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


@dataclass(frozen=True)
class TimelineStepView:
    """One kickoff-timeline row: when, what, and the recipe it links to."""

    label: str
    task: str
    recipe: str  # "recipe:<id>" label, or "" for a general task
    minutes: int | None  # minutes from kickoff, only when the time maps to a clock


@dataclass(frozen=True)
class MenuView:
    """A game-day menu or a division dish-off card."""

    label: str
    title: str
    subtitle: str
    recipes: tuple[Ref, ...]
    why_it_works: str
    prep_plan: str
    description: str
    prep_note: str
    timeline: tuple[TimelineStepView, ...]


@dataclass(frozen=True)
class TeamView:
    label: str
    name: str
    location: str
    recipes: tuple[Ref, ...]


# ------------------------------------------------------------------------------ pages
@dataclass(frozen=True)
class WebsiteLink:
    href: str
    display: str
    edition: str


@dataclass(frozen=True)
class BookStats:
    recipes: int
    teams: int
    components: int
    menus: int


@dataclass(frozen=True)
class CoverView(PageView):
    title: str
    subtitle: str
    tagline: str
    body: str
    website: WebsiteLink | None
    stats: BookStats

    @property
    def page_title(self) -> str:
        return self.title


@dataclass(frozen=True)
class ContentsTeam:
    name: str
    recipes: tuple[Ref, ...]


@dataclass(frozen=True)
class ContentsDivision:
    ref: Ref
    teams: tuple[ContentsTeam, ...]


@dataclass(frozen=True)
class ContentsView(PageView):
    label: str
    indexes: tuple[Ref, ...]
    divisions: tuple[ContentsDivision, ...]
    game_day: Ref
    make_buy: Ref

    @property
    def page_title(self) -> str:
        return "All recipes"


@dataclass(frozen=True)
class IndexSectionView:
    title: str
    entries: tuple[Ref, ...]


@dataclass(frozen=True)
class IndexView(PageView):
    label: str
    title: str
    intro: str
    sections: tuple[IndexSectionView, ...]

    @property
    def page_title(self) -> str:
        return self.title


@dataclass(frozen=True)
class DivisionView(PageView):
    label: str
    end_label: str | None
    name: str
    conference: str
    teams: tuple[TeamView, ...]
    dishoffs: tuple[MenuView, ...]

    @property
    def page_title(self) -> str:
        return self.name


@dataclass(frozen=True)
class MenuPageView(PageView):
    """One page of game-day menus of a single type."""

    type_title: str
    end_label: str
    menus: tuple[MenuView, ...]

    @property
    def page_title(self) -> str:
        return self.type_title


@dataclass(frozen=True)
class MenuGroupView:
    title: str
    description: str
    menus: tuple[Ref, ...]


@dataclass(frozen=True)
class GameDayIndexView(PageView):
    label: str
    groups: tuple[MenuGroupView, ...]

    @property
    def page_title(self) -> str:
        return "Game Day Menus"


@dataclass(frozen=True)
class MakeBuyComponent:
    ref: Ref
    used_in: tuple[str, ...]
    used_in_refs: tuple[Ref, ...]


@dataclass(frozen=True)
class MakeBuyKind:
    title: str
    components: tuple[MakeBuyComponent, ...]


@dataclass(frozen=True)
class MakeBuyView(PageView):
    label: str
    kinds: tuple[MakeBuyKind, ...]

    @property
    def page_title(self) -> str:
        return "Make It or Buy It"


@dataclass(frozen=True)
class RecipeView(PageView):
    """A recipe, as every format shows it."""

    label: str
    end_label: str | None
    title: str
    team: str
    location: str
    course: str
    division: str
    meta_line: str
    meta: tuple[tuple[str, str], ...]
    description: str
    image: str
    image_size: int
    photo_credit: str
    quick_options: tuple[OptionView, ...]
    groups: tuple[GroupView, ...]
    compact_ingredients: bool
    instructions: str
    kitchen_notes: str
    source: SourceView | None
    web: WebView | None
    qr: str

    @property
    def page_title(self) -> str:
        return self.title


@dataclass(frozen=True)
class ComponentView(PageView):
    """A Make It or Buy It component, as every format shows it."""

    label: str
    title: str
    description: str
    kind: str  # the kind's singular name
    kind_id: str
    meta_line: str
    meta: tuple[tuple[str, str], ...]
    groups: tuple[GroupView, ...]
    method: str
    note: str
    quick_buy: str
    used_in: tuple[Ref, ...]
    source: SourceView | None
    web: WebView | None
    qr: str

    @property
    def page_title(self) -> str:
        return self.title


@dataclass(frozen=True)
class ComponentLink:
    title: str
    href: str | None


@dataclass(frozen=True)
class CardView(RecipeView):
    """A recipe card: the base recipe plus where each component can be found."""

    component_links: Mapping[str, ComponentLink]
    recipe_file: str  # the recipe's file, named by the manifest's overflow errors
