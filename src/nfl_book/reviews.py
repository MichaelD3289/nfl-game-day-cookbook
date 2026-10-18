"""Review age: published recipes and components whose last review is missing or old.

``last_reviewed_at`` records the last completed source review. When
``review_max_age_days`` is set in ``data/book.yml``, validation warns (never
errors) about each published item past the limit. :func:`current_date` is the
only clock, so tests can pin it.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from typing import Literal

from nfl_book.errors import Diagnostics
from nfl_book.models.common import Status
from nfl_book.models.content import Component, Content, Recipe

ReviewKind = Literal["recipe", "component"]


def current_date() -> date:
    """Today's date: the one place review checks read the clock."""
    return date.today()


def _today(today: date | None) -> date:
    # current_date is a module global resolved at call time, so tests can monkeypatch it.
    return today if today is not None else current_date()


@dataclass(frozen=True)
class StaleReview:
    """A published item whose review is missing (``age_days`` is None) or too old."""

    kind: ReviewKind
    item: Recipe | Component
    age_days: int | None

    @property
    def last_reviewed_at(self) -> date | None:
        return self.item.meta.last_reviewed_at


def _published(
    recipes: Iterable[Recipe], components: Iterable[Component]
) -> list[tuple[ReviewKind, Recipe | Component]]:
    items: list[tuple[ReviewKind, Recipe | Component]] = []
    items += [("recipe", r) for r in recipes if r.meta.status is Status.PUBLISHED]
    items += [("component", c) for c in components if c.meta.status is Status.PUBLISHED]
    return items


def _sort_key(stale: StaleReview) -> tuple[int, int, int, str]:
    never = stale.age_days is None
    return (
        0 if never else 1,
        -(stale.age_days or 0),
        0 if stale.kind == "recipe" else 1,
        stale.item.id,
    )


def stale_reviews(
    recipes: Iterable[Recipe],
    components: Iterable[Component],
    max_age_days: int,
    today: date | None = None,
) -> list[StaleReview]:
    """Published items never reviewed or reviewed more than ``max_age_days`` ago.

    Never-reviewed items come first, then the oldest reviews; ties list recipes
    before components, then sort by id. Future dates are not stale.
    """
    now = _today(today)
    result = []
    for kind, item in _published(recipes, components):
        reviewed = item.meta.last_reviewed_at
        if reviewed is None:
            result.append(StaleReview(kind, item, None))
            continue
        age = (now - reviewed).days
        if age > max_age_days:
            result.append(StaleReview(kind, item, age))
    return sorted(result, key=_sort_key)


def check_review_ages(
    content: Content,
    max_age_days: int | None,
    diags: Diagnostics,
    today: date | None = None,
) -> None:
    """Warn about published items with a missing, too old or future review date."""
    if max_age_days is None:
        return
    now = _today(today)
    for _, item in _published(content.recipes, content.components):
        reviewed = item.meta.last_reviewed_at
        if reviewed is not None and reviewed > now:
            diags.warning(
                "review", f"last_reviewed_at {reviewed} is after today ({now})", item.path
            )
    for stale in stale_reviews(content.recipes, content.components, max_age_days, now):
        if stale.age_days is None:
            message = (
                f"published {stale.kind} has no last_reviewed_at; the limit is "
                f"{max_age_days} days (review_max_age_days in data/book.yml)"
            )
        else:
            message = (
                f"last_reviewed_at {stale.last_reviewed_at} is {stale.age_days} days ago, "
                f"over the {max_age_days}-day limit; re-check its source, product names "
                "and amounts"
            )
        diags.warning("review", message, stale.item.path)
