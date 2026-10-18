"""Pydantic schemas (the authoring contract) and parsed document types."""

from nfl_book.models.common import SLUG_PATTERN, SourceLink, Status
from nfl_book.models.config import (
    BookConfig,
    Bucket,
    ComponentKind,
    IndexConfig,
    MenuType,
)
from nfl_book.models.content import (
    Component,
    ComponentMeta,
    Content,
    CoverPage,
    DishOff,
    DishOffMeta,
    GameDayMenu,
    GameDayMenuMeta,
    Ingredient,
    IngredientGroup,
    Recipe,
    RecipeMeta,
    TimelineStep,
)
from nfl_book.models.nfl import Division, League, Team

__all__ = [
    "SLUG_PATTERN",
    "BookConfig",
    "Bucket",
    "Component",
    "ComponentKind",
    "ComponentMeta",
    "Content",
    "CoverPage",
    "DishOff",
    "DishOffMeta",
    "Division",
    "GameDayMenu",
    "GameDayMenuMeta",
    "IndexConfig",
    "Ingredient",
    "IngredientGroup",
    "League",
    "MenuType",
    "Recipe",
    "RecipeMeta",
    "SourceLink",
    "Status",
    "Team",
    "TimelineStep",
]
