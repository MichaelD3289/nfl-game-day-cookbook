from types import SimpleNamespace
from typing import Any

from nfl_book.models.content import Ingredient, IngredientGroup, TimelineStep
from nfl_book.render.pages import COMPACT_INGREDIENTS_OVER, TimelineStepView, _compact, _timeline


def _groups(*sizes: int) -> tuple[IngredientGroup, ...]:
    return tuple(
        IngredientGroup(f"G{n}", tuple(Ingredient(f"item {i}", None) for i in range(size)))
        for n, size in enumerate(sizes)
    )


def test_short_ingredient_lists_stay_bulleted() -> None:
    assert not _compact(_groups(COMPACT_INGREDIENTS_OVER))


def test_long_ingredient_lists_across_groups_are_compacted() -> None:
    assert _compact(_groups(COMPACT_INGREDIENTS_OVER, 1))


def test_timeline_views_label_link_and_clock_minutes() -> None:
    steps = [
        TimelineStep(at="-1d", task="Make the dip.", recipe="test-buffalo-sliders"),
        TimelineStep(at="-1h30m", task="Marinate.", recipe="test-missing"),
        TimelineStep(at="halftime", task="Reheat."),
    ]
    model: Any = SimpleNamespace(recipes_by_id={"test-buffalo-sliders": object()})
    menu: Any = SimpleNamespace(meta=SimpleNamespace(timeline=steps))
    assert _timeline(model, menu) == [
        TimelineStepView("Day before", "Make the dip.", "recipe:test-buffalo-sliders", None),
        TimelineStepView("1 hr 30 min before", "Marinate.", "", -90),
        TimelineStepView("Halftime", "Reheat.", "", None),
    ]


def test_menu_without_timeline_has_no_steps() -> None:
    model: Any = SimpleNamespace(recipes_by_id={})
    assert _timeline(model, SimpleNamespace(meta=SimpleNamespace(timeline=None))) == []
