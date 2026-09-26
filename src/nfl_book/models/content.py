"""Schemas for authored content (recipes, components, menus, dish-offs).

Front-matter models are the contract authors write against; ``extra="forbid"``
turns typos into validation errors instead of silently ignored keys.
Ownership (team, component kind, menu type, division) is *not* part of the
front matter: it is inferred from the file's location by discovery.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from pydantic import Field, model_validator

from nfl_book.models.common import HttpUrlStr, NonEmpty, Slug, SourceLink, Status, StrictModel
from nfl_book.models.config import ComponentKind, MenuType
from nfl_book.models.nfl import Division, Team


class RecipeMeta(StrictModel):
    id: Slug
    title: NonEmpty
    status: Status
    course: Slug
    location: str | None = Field(None, description="Overrides the team's location text.")
    yield_: NonEmpty = Field(alias="yield")
    prep: str | None = None
    cook: str | None = None
    index: dict[str, Slug | list[Slug]] = Field(
        default_factory=dict, description="Index bucket ids keyed by index field name."
    )
    image: str | None = Field(None, description="Path relative to this recipe file.")
    photo_credit: str | None = None
    source: SourceLink | None = None
    quick_options: dict[Slug, NonEmpty] = Field(
        default_factory=dict,
        description="Per-recipe override of a referenced component's quick-buy text.",
    )
    order: int | None = Field(None, description="Optional sort key within the team.")

    @model_validator(mode="after")
    def _credit_required(self) -> RecipeMeta:
        if self.image and not self.photo_credit:
            raise ValueError("`image` requires `photo_credit`")
        return self


class ComponentMeta(StrictModel):
    id: Slug
    title: NonEmpty
    status: Status
    yield_: str | None = Field(None, alias="yield")
    source: SourceLink | None = None
    quick_buy: NonEmpty = Field(description="Store-bought shortcut shown in Quick Options.")
    always_include: bool = False
    order: int | None = None


class GameDayMenuMeta(StrictModel):
    id: Slug
    title: NonEmpty
    subtitle: str | None = Field(None, description="Matchup / team context line.")
    status: Status = Status.PUBLISHED
    recipes: list[Slug] = Field(min_length=1)
    why_it_works: str | None = None
    prep_plan: str | None = None
    order: int | None = None


class DishOffMeta(StrictModel):
    id: Slug
    title: NonEmpty
    status: Status = Status.PUBLISHED
    recipes: list[Slug] = Field(min_length=1)
    description: str | None = None
    prep_note: str | None = None
    order: int | None = None


# Parsed documents ------------------------------------------------------------


@dataclass(frozen=True)
class Ingredient:
    """One ingredient line. ``text`` is Markdown with any component marker removed."""

    text: str
    component: str | None = None


@dataclass(frozen=True)
class IngredientGroup:
    heading: str | None
    items: tuple[Ingredient, ...]


def _component_refs(groups: tuple[IngredientGroup, ...]) -> tuple[str, ...]:
    seen: dict[str, None] = {}
    for group in groups:
        for item in group.items:
            if item.component:
                seen.setdefault(item.component, None)
    return tuple(seen)


@dataclass(frozen=True)
class Recipe:
    meta: RecipeMeta
    path: Path
    division: Division
    team: Team
    ingredients: tuple[IngredientGroup, ...]
    instructions: str
    kitchen_notes: str | None = None

    @property
    def id(self) -> str:
        return self.meta.id

    @property
    def title(self) -> str:
        return self.meta.title

    @property
    def location(self) -> str:
        return self.meta.location or self.team.location

    @property
    def component_refs(self) -> tuple[str, ...]:
        """Referenced component ids in first-use order (drives the Quick Options card)."""
        return _component_refs(self.ingredients)


@dataclass(frozen=True)
class Component:
    meta: ComponentMeta
    path: Path
    kind: ComponentKind
    ingredients: tuple[IngredientGroup, ...]
    method: str
    note: str | None = None

    @property
    def id(self) -> str:
        return self.meta.id

    @property
    def title(self) -> str:
        return self.meta.title

    @property
    def component_refs(self) -> tuple[str, ...]:
        return _component_refs(self.ingredients)


@dataclass(frozen=True)
class GameDayMenu:
    meta: GameDayMenuMeta
    path: Path
    menu_type: MenuType

    @property
    def id(self) -> str:
        return self.meta.id


@dataclass(frozen=True)
class DishOff:
    meta: DishOffMeta
    path: Path
    division: Division

    @property
    def id(self) -> str:
        return self.meta.id


@dataclass(frozen=True)
class CoverPage:
    title: str
    subtitle: str | None
    tagline: str | None
    body: str


@dataclass
class Content:
    """Everything discovered and parsed from the content root (all statuses)."""

    recipes: list[Recipe] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)
    menus: list[GameDayMenu] = field(default_factory=list)
    dishoffs: list[DishOff] = field(default_factory=list)
    cover: CoverPage | None = None


__all__ = [
    "Component",
    "ComponentMeta",
    "Content",
    "CoverPage",
    "DishOff",
    "DishOffMeta",
    "GameDayMenu",
    "GameDayMenuMeta",
    "HttpUrlStr",
    "Ingredient",
    "IngredientGroup",
    "Recipe",
    "RecipeMeta",
]
