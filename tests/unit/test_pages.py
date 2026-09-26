from nfl_book.models.content import Ingredient, IngredientGroup
from nfl_book.render.pages import COMPACT_INGREDIENTS_OVER, _compact


def _groups(*sizes: int) -> tuple[IngredientGroup, ...]:
    return tuple(
        IngredientGroup(f"G{n}", tuple(Ingredient(f"item {i}", None) for i in range(size)))
        for n, size in enumerate(sizes)
    )


def test_short_ingredient_lists_stay_bulleted() -> None:
    assert not _compact(_groups(COMPACT_INGREDIENTS_OVER))


def test_long_ingredient_lists_across_groups_are_compacted() -> None:
    assert _compact(_groups(COMPACT_INGREDIENTS_OVER, 1))
