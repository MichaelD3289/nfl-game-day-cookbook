"""Unit conversion in styles/website-scale.js, run through Node.

The website scales amounts in the browser, so the conversion rules live in JavaScript.
These tests need Node.js and are skipped when it is not installed.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from nfl_book.project import Project
from nfl_book.quantities import UNITS
from nfl_book.website import build_website

SCRIPT = Path(__file__).resolve().parents[2] / "styles" / "website-scale.js"
NODE = shutil.which("node")
pytestmark = pytest.mark.skipif(NODE is None, reason="Node.js is not installed")


def node(expression: str) -> Any:
    assert NODE is not None
    program = (
        f"const s = require({json.dumps(str(SCRIPT))});\n"
        f"process.stdout.write(JSON.stringify({expression}));"
    )
    result = subprocess.run(
        [NODE, "-e", program], capture_output=True, text=True, check=True, timeout=30
    )
    return json.loads(result.stdout)


CASES = [
    # (low, high, unit, factor, expected)
    (4, None, "tsp", 3, "¼ cup"),  # 12 teaspoons
    (12, None, "tsp", 1, "¼ cup"),
    (3, None, "tbsp", 2, "6 tablespoons"),
    (7, None, "tsp", 1, "2 tablespoons + 1 teaspoon"),
    (5, None, "tsp", 1, "1 tablespoon + 2 teaspoons"),
    (1, None, "tsp", 1.5, "1½ teaspoons"),
    (1, None, "tbsp", 0.5, "1½ teaspoons"),
    (1, None, "tsp", 1 / 3, "¼ teaspoon"),
    (1, None, "cup", 4 / 3, "1⅓ cups"),
    (1.125, None, "cup", 2, "2¼ cups"),
    (0.25, None, "cup", 3, "¾ cup"),
    (4, None, "oz", 3, "¾ pound"),
    (4, None, "oz", 1.5, "6 ounces"),
    (0.25, None, "lb", 0.5, "2 ounces"),
    (2.5, None, "lb", 2, "5 pounds"),
    (4, None, "cup", 3, "12 cups"),  # cups never become quarts
    (2, None, "quart", 0.5, "1 quart"),
    (575, None, "g", 2, "1.15 kg"),
    (575, None, "g", 0.5, "290 g"),
    (88, None, "ml", 3, "265 ml"),
    (2, 3, "cup", 2, "4–6 cups"),
    (2, 3, "tbsp", 2, "4–6 tablespoons"),
    (1, None, None, 1.5, "1–2"),
    (1, None, None, 0.5, "½"),
    (3, None, None, 2, "6"),
    (2, 3, None, 2, "4–6"),
    (2, 3, None, 1.5, "3–5"),
]


def test_conversions() -> None:
    calls = ", ".join(
        f"s.scale({{low: {low}, high: {json.dumps(high)}, unit: {json.dumps(unit)}}}, {factor})"
        for low, high, unit, factor, _ in CASES
    )
    results = node(f"[{calls}]")
    assert results == [case[-1] for case in CASES]


def test_adjective_is_kept() -> None:
    result = node('s.scale({low: 1, high: null, unit: "tbsp", adjective: "generous"}, 2)')
    assert result == "2 generous tablespoons"


def test_scale_factors_from_links() -> None:
    assert node('["2", "3/2", "4/3", "0", "x", "1000"].map(s.parseFactor)') == [
        2,
        1.5,
        4 / 3,
        None,
        None,
        None,
    ]
    assert node("[2, 0.5, 1.5, 4/3].map(s.describe)") == ["2×", "½×", "1½×", "1⅓×"]
    assert node('["10/4", "8/4", "3", "12/6"].map(s.reduce)') == ["5/2", "2", "3", "2"]


def test_units_match_the_parser() -> None:
    units = node(
        "Object.fromEntries(Object.entries(s.UNITS).map(([k, u]) => [k, [u.kind, u.size]]))"
    )
    assert units == {key: [kind, int(size)] for key, (kind, size) in UNITS.items()}


def test_print_label_names_scale_and_servings() -> None:
    assert node(
        "[s.printLabel(2, 6, 6), s.printLabel(2, 4, 6), s.printLabel(1.5, null, null),"
        " s.printLabel(2.5, 4, 4)]"
    ) == [
        "Scaled 2× · serves 12",
        "Scaled 2× · serves 8–12",
        "Scaled 1½×",
        "Scaled 2½× · serves 10",
    ]


@pytest.mark.parametrize(
    ("factor", "expected"),
    [
        (0.5, [["½", "10 tablespoons"], ["2 tablespoons"], ["½", "1¾ cups"], []]),
        (2, [["2", "2½ cups"], ["½ cup"], ["2", "7 cups"], []]),
    ],
)
def test_quick_component_choices_scale_from_generated_markup(
    fixture_book: Project, factor: float, expected: list[list[str]]
) -> None:
    recipe = next(fixture_book.recipes_dir.rglob("test-citrus-wings.md"))
    ref = "{{component:test-wing-sauce}}"
    choices = [
        "1 batch homemade test sauce (about 1 1/4 cups); "
        f"or substitute the same amount of store-bought sauce {ref}",
        f"1/4 cup homemade test sauce; or substitute the same amount of store-bought sauce {ref}",
        "1 batch homemade test sauce (about 3 1/2 cups); "
        f"or substitute store-bought soup (two 10–10.5-ounce cans per homemade batch) {ref}",
        f"Homemade test sauce, 2–3 tablespoons per roll; or substitute store-bought sauce {ref}",
    ]
    recipe.write_text(
        recipe.read_text().replace(
            f"- 1 cup wing sauce {ref}", "\n".join("- " + line for line in choices)
        )
    )
    site = build_website(fixture_book, render=False).document.parent
    page = (site / "recipe-test-citrus-wings.qmd").read_text()
    lines = [line for line in page.splitlines() if "; or substitute" in line]
    assert len(lines) == len(choices)
    amounts = []
    for line in lines:
        assert line.index('class="q-mark"') > line.index("; or substitute")
        assert "data-carry-scale" in line
        row = []
        for attributes in re.findall(r'<span class="qty" ([^>]+)>', line):
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', attributes))
            row.append(
                {
                    "low": float(Fraction(attrs["data-q"])),
                    "high": None,
                    "unit": attrs.get("data-unit"),
                }
            )
        amounts.append(row)
    assert "two 10–10.5-ounce cans per homemade batch" in lines[2]
    assert "2–3 tablespoons per roll" in lines[3]
    result = node(f"{json.dumps(amounts)}.map(row => row.map(amount => s.scale(amount, {factor})))")
    assert result == expected
