"""Build-time parsing of ingredient amounts and servings for website scaling."""

from __future__ import annotations

from fractions import Fraction

import pytest

from nfl_book.quantities import (
    find_amounts,
    find_yield_amounts,
    parse_number,
    parse_servings,
    servings_from_yield,
)


def shown(text: str) -> list[tuple[str, Fraction, Fraction | None, str | None]]:
    amounts, problems = find_amounts(text)
    assert problems == []
    return [(text[a.start : a.end], a.low, a.high, a.unit) for a in amounts]


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("2", Fraction(2)),
        ("1.5", Fraction(3, 2)),
        ("3/4", Fraction(3, 4)),
        ("1 1/2", Fraction(3, 2)),
        ("½", Fraction(1, 2)),
        ("2½", Fraction(5, 2)),
        ("1 ⅓", Fraction(4, 3)),
    ],
)
def test_numbers(text: str, value: Fraction) -> None:
    assert parse_number(text) == value


def test_measured_amount_at_start() -> None:
    assert shown("1 1/2 cups beef broth") == [("1 1/2 cups", Fraction(3, 2), None, "cup")]


def test_count_at_start() -> None:
    assert shown("3 large garlic cloves, minced") == [("3", Fraction(3), None, None)]
    assert shown("1 (15-ounce) can tomato sauce") == [("1", Fraction(1), None, None)]


def test_ranges_keep_both_ends() -> None:
    assert shown("2 to 3 cups water") == [("2 to 3 cups", Fraction(2), Fraction(3), "cup")]
    assert shown("2–4 garlic cloves") == [("2–4", Fraction(2), Fraction(4), None)]
    assert shown("1 1/4–1 1/2 cups sauce") == [
        ("1 1/4–1 1/2 cups", Fraction(5, 4), Fraction(3, 2), "cup")
    ]


def test_qualifiers_before_the_amount() -> None:
    assert shown("About ½ teaspoon kosher salt") == [("½ teaspoon", Fraction(1, 2), None, "tsp")]
    assert shown("Optional: 1/4 cup banana peppers") == [("1/4 cup", Fraction(1, 4), None, "cup")]
    assert shown("Juice of 2 lemons") == [("2", Fraction(2), None, None)]


def test_adjective_between_amount_and_unit_is_kept() -> None:
    amounts, _ = find_amounts("1 generous tablespoon olive oil")
    assert amounts[0].unit == "tbsp"
    assert amounts[0].adjective == "generous"


def test_equivalents_in_brackets_scale_too() -> None:
    assert shown("575 grams (3 cups) sugar") == [
        ("575 grams", Fraction(575), None, "g"),
        ("3 cups", Fraction(3), None, "cup"),
    ]
    assert shown("2 medium tomatoes (about 12 ounces), diced") == [
        ("2", Fraction(2), None, None),
        ("12 ounces", Fraction(12), None, "oz"),
    ]


def test_package_sizes_and_portions_do_not_scale() -> None:
    assert shown("1 can (15 ounces) tomato sauce") == [("1", Fraction(1), None, None)]
    assert shown("4 tablespoons mustard (1 tablespoon per sandwich)") == [
        ("4 tablespoons", Fraction(4), None, "tbsp")
    ]
    assert shown("Rémoulade, 2–3 tablespoons per roll") == []
    assert shown("3 tablespoons ice water, plus more ½ tablespoon at a time") == [
        ("3 tablespoons", Fraction(3), None, "tbsp")
    ]


def test_each_before_the_items_is_a_total() -> None:
    assert shown("1 teaspoon each cumin and paprika") == [("1 teaspoon", Fraction(1), None, "tsp")]


def test_plus_joins_one_amount() -> None:
    assert shown("1 cup plus 2 tablespoons water") == [
        ("1 cup plus 2 tablespoons", Fraction(9, 8), None, "cup")
    ]
    # Different ingredients are not joined.
    assert len(shown("4 cups ice plus 1 cup water")) == 2


def test_sizes_and_temperatures_are_not_amounts() -> None:
    assert shown("Oil to 3/4-inch depth") == []
    assert shown("1 round 8–10-inch loaf") == [("1", Fraction(1), None, None)]
    assert shown("2 inches of oil") == []
    assert shown("Salt, to taste") == []


@pytest.mark.parametrize(
    "text",
    ["500g flour", "2tbsp butter", "1/ cup sugar", "1/0 cup sugar", "3–2 cups flour"],
)
def test_unreadable_amounts_are_problems(text: str) -> None:
    _, problems = find_amounts(text)
    assert problems


def test_servings_field() -> None:
    assert parse_servings(6) == (6, 6)
    assert parse_servings("6-8") == (6, 8)
    assert parse_servings("6 to 8") == (6, 8)
    assert parse_servings(0) is None
    assert parse_servings("8-6") is None
    assert parse_servings("a few") is None


@pytest.mark.parametrize(
    ("text", "servings"),
    [
        ("4 servings", (4, 4)),
        ("6–8 servings", (6, 8)),
        ("1 serving", (1, 1)),
        ("4–6 side servings; enough for sandwiches", (4, 6)),
        ("4 people", (4, 4)),
        ("1 casserole; serves 6–10", (6, 10)),
        ("2 pounds wings, about 4 appetizer portions", (4, 4)),
        ("12 sliders", None),
        ("See recipe", None),
        ("About 1½ cups", None),
    ],
)
def test_servings_from_yield(text: str, servings: tuple[int, int] | None) -> None:
    assert servings_from_yield(text) == servings


@pytest.mark.parametrize(
    ("text", "scaled"),
    [
        ("16 pretzels", ["16"]),
        ("About 1 1/2 cups (estimated)", ["1 1/2 cups"]),
        ("8 large or 12 standard rolls", ["8", "12"]),
        ("1 casserole; serves 6–10", ["1", "6–10"]),
        ("10 servings (10 brats)", ["10", "10"]),
        ("4 servings (4 shrimp each)", ["4"]),
        ("12 tenders; use two per sub", ["12"]),
        ("332 g dough, enough for two 12-inch pizzas", ["332 g"]),
        ("5 servings (15 pounds crawfish; half a 30-pound batch)", ["5", "15 pounds"]),
        ("One 12- to 13-inch pizza", []),
        ("One 13-by-9-inch pan", []),
        ("See recipe", []),
    ],
)
def test_yield_amounts(text: str, scaled: list[str]) -> None:
    assert [text[a.start : a.end] for a in find_yield_amounts(text)] == scaled
