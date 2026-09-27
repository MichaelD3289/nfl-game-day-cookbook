"""``nfl-book stats``: where the synthetic sample book is thin."""

from __future__ import annotations

import json
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from nfl_book.errors import ValidationFailed
from nfl_book.project import Project
from nfl_book.stats import (
    Column,
    Report,
    Section,
    Thresholds,
    build_report,
    render_json,
    render_markdown,
)

Write = Callable[[str, str], Path]

PACKERS_RECIPE = """---
id: test-brat-dip
title: Test Brat Dip
status: {status}
course: {course}
yield: 1 bowl
---

## Ingredients

- 2 bratwursts

## Instructions

Mix.
"""


def rows(report: Report, section_id: str) -> list[dict[str, Any]]:
    return report.section(section_id).records()


def by_team(report: Report) -> dict[str, dict[str, Any]]:
    return {row["team"]: row for row in rows(report, "teams")}


def test_sections_in_order(fixture_book: Project) -> None:
    report = build_report(fixture_book)
    assert [s.id for s in report.sections] == [
        "teams",
        "course-gaps",
        "dish-off-gaps",
        "index-course",
        "index-main-ingredient",
        "index-practical-time",
        "index-ingredient-cost",
        "components",
        "unreferenced-components",
        "menu-type-gaps",
        "stale-reviews",
    ]
    assert report.section("index-course").title == "Index by Course"


def test_team_counts_fewest_first(fixture_book: Project) -> None:
    table = rows(build_report(fixture_book), "teams")
    assert len(table) == 32
    assert table[0] == {
        "team": "New England Patriots",
        "division": "AFC East",
        "published": 0,
        "testing": 0,
        "draft": 0,
        "total": 0,
    }
    assert [r["team"] for r in table[-3:]] == [
        "New York Jets",
        "Buffalo Bills",
        "Miami Dolphins",
    ]
    assert table[-3]["draft"] == 1
    assert sum(r["published"] for r in table) == 2
    assert sum(r["testing"] for r in table) == 0
    assert sum(r["draft"] for r in table) == 1


def test_testing_status_counted(fixture_book: Project, write: Write) -> None:
    write(
        "recipes/nfc/north/packers/test-brat-dip.md",
        PACKERS_RECIPE.format(status="testing", course="desserts"),
    )
    report = build_report(fixture_book)
    packers = by_team(report)["Green Bay Packers"]
    assert (packers["testing"], packers["total"]) == (1, 1)
    gaps = {r["team"]: r["missing"] for r in rows(report, "course-gaps")}
    assert gaps["Green Bay Packers"] == ("Appetizers", "Sides", "Meals")


def test_retired_not_counted(fixture_book: Project, write: Write) -> None:
    write(
        "recipes/nfc/north/packers/test-brat-dip.md",
        PACKERS_RECIPE.format(status="retired", course="desserts"),
    )
    report = build_report(fixture_book)
    assert by_team(report)["Green Bay Packers"]["total"] == 0
    assert sum(r["recipes"] for r in rows(report, "index-course")) == 3


def test_course_gaps(fixture_book: Project) -> None:
    table = rows(build_report(fixture_book), "course-gaps")
    gaps = {r["team"]: r["missing"] for r in table}
    assert len(table) == 32
    assert gaps["Buffalo Bills"] == ("Sides", "Meals", "Desserts")
    assert gaps["Miami Dolphins"] == ("Appetizers", "Sides", "Desserts")
    assert gaps["New York Jets"] == ("Sides", "Meals", "Desserts")
    assert gaps["New England Patriots"] == ("Appetizers", "Sides", "Meals", "Desserts")
    assert sum(len(m) for m in gaps.values()) == 125


def test_dishoff_gaps(fixture_book: Project) -> None:
    table = rows(build_report(fixture_book), "dish-off-gaps")
    assert len(table) == 8
    assert table[0] == {"division": "AFC East", "dish_offs": 1}
    assert all(r["dish_offs"] == 0 for r in table[1:])
    assert rows(build_report(fixture_book, Thresholds(min_dishoffs=1)), "dish-off-gaps")[0] == {
        "division": "AFC North",
        "dish_offs": 0,
    }


def test_index_spread(fixture_book: Project) -> None:
    report = build_report(fixture_book)
    assert rows(report, "index-course") == [
        {"bucket": "Appetizers", "recipes": 2, "note": ""},
        {"bucket": "Sides", "recipes": 0, "note": "thin"},
        {"bucket": "Meals", "recipes": 1, "note": ""},
        {"bucket": "Desserts", "recipes": 0, "note": "thin"},
    ]
    main = rows(report, "index-main-ingredient")
    assert {"bucket": "Poultry", "recipes": 2, "note": ""} in main
    assert main[-1] == {"bucket": "(not set)", "recipes": 1, "note": ""}
    cost = rows(report, "index-ingredient-cost")
    assert [(r["bucket"], r["recipes"], r["note"]) for r in cost] == [
        ("Pantry Friendly", 1, ""),
        ("Moderate", 1, ""),
        ("Premium", 0, "thin"),
        ("(not set)", 1, ""),
    ]


def test_component_usage(fixture_book: Project) -> None:
    table = rows(build_report(fixture_book), "components")
    assert [(r["id"], r["kind"], r["status"], r["direct"], r["total"]) for r in table] == [
        ("test-wing-sauce", "Sauces", "published", 1, 1),
        ("test-blue-cheese-dip", "Dips", "published", 1, 1),
        ("test-cajun-seasoning", "Seasonings", "published", 0, 1),
        ("test-draft-side", "Sides", "draft", 1, 1),
    ]
    assert table[0]["component"] == "Test Wing Sauce"
    assert rows(build_report(fixture_book), "unreferenced-components") == []


def test_unreferenced_components(fixture_book: Project) -> None:
    wings = fixture_book.content_root / "recipes/afc/east/dolphins/test-citrus-wings.md"
    wings.write_text(
        wings.read_text().replace(" {{component:test-wing-sauce}}", ""), encoding="utf-8"
    )
    report = build_report(fixture_book)
    table = rows(report, "components")
    assert [r["id"] for r in table[:2]] == ["test-wing-sauce", "test-cajun-seasoning"]
    assert all(r["total"] == 0 for r in table[:2])
    assert [r["id"] for r in rows(report, "unreferenced-components")] == [
        "test-wing-sauce",
        "test-cajun-seasoning",
    ]


def test_menu_type_gaps(fixture_book: Project) -> None:
    table = rows(build_report(fixture_book), "menu-type-gaps")
    assert len(table) == 6
    assert {"menu_type": "Fast Day", "menus": 1} in table
    relaxed = rows(build_report(fixture_book, Thresholds(min_menus=1)), "menu-type-gaps")
    assert len(relaxed) == 5
    assert "Fast Day" not in [r["menu_type"] for r in relaxed]


def test_invalid_content_raises(fixture_book: Project) -> None:
    path = fixture_book.content_root / "recipes/afc/east/bills/test-buffalo-sliders.md"
    path.write_text(path.read_text().replace("course:", "course_typo:"), encoding="utf-8")
    with pytest.raises(ValidationFailed) as info:
        build_report(fixture_book)
    paths = [d.path for d in info.value.diagnostics.errors]
    assert any(p is not None and p.name == "test-buffalo-sliders.md" for p in paths)


def test_does_not_write_outputs(fixture_book: Project) -> None:
    build_report(fixture_book)
    assert not fixture_book.generated_dir.exists()
    assert not fixture_book.dist_dir.exists()


def test_markdown_escapes_and_empty() -> None:
    report = Report(
        Thresholds(),
        (
            Section(
                "demo",
                "Demo",
                (Column("name", "Name"), Column("tags", "Tags")),
                (("a|b", ("x", "y")),),
            ),
            Section("none", "Nothing", (Column("name", "Name"),), (), empty="All good."),
        ),
    )
    text = render_markdown(report)
    assert "## Demo" in text
    assert "| Name | Tags |" in text
    assert "| a\\|b | x, y |" in text
    assert "## Nothing\n\nAll good." in text


def test_markdown_renders_none_as_empty_cell() -> None:
    columns = (Column("item", "Item"), Column("age_days", "Age (days)"))
    report = Report(Thresholds(), (Section("demo", "Demo", columns, (("Sauce", None),)),))
    assert "| Sauce |  |" in render_markdown(report)


def test_json_roundtrip(fixture_book: Project) -> None:
    data = json.loads(render_json(build_report(fixture_book, Thresholds(min_menus=4))))
    assert data["thresholds"] == {
        "min_dishoffs": 2,
        "min_menus": 4,
        "thin_share": 0.1,
        "today": "2026-09-27",
    }
    teams = data["sections"][0]
    assert (teams["id"], teams["title"]) == ("teams", "Recipes per team")
    assert teams["rows"][0]["team"] == "New England Patriots"
    gaps = next(s for s in data["sections"] if s["id"] == "course-gaps")
    assert gaps["rows"][0]["missing"] == ["Sides", "Meals", "Desserts"]
    stale = next(s for s in data["sections"] if s["id"] == "stale-reviews")
    assert stale["rows"] == []


def set_reviewed(project: Project, relative: str, value: str | None) -> None:
    path = project.content_root / relative
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out = [
        (f"last_reviewed_at: {value}\n" if value else "")
        if line.startswith("last_reviewed_at:")
        else line
        for line in lines
    ]
    assert out != lines
    path.write_text("".join(out), encoding="utf-8")


SLIDERS = "recipes/afc/east/bills/test-buffalo-sliders.md"
WINGS = "recipes/afc/east/dolphins/test-citrus-wings.md"
SAUCE = "components/sauces/test-wing-sauce.md"


def stale_rows(report: Report) -> list[tuple[Any, ...]]:
    return [
        (r["item"], r["kind"], r["id"], r["last_reviewed"], r["age_days"])
        for r in rows(report, "stale-reviews")
    ]


def test_stale_reviews_stalest_first(fixture_book: Project) -> None:
    set_reviewed(fixture_book, SLIDERS, "2025-01-01")
    set_reviewed(fixture_book, WINGS, "2025-09-26")
    set_reviewed(fixture_book, SAUCE, None)
    report = build_report(fixture_book)
    section = report.section("stale-reviews")
    assert section.title == "Published items not reviewed in 365 days (stalest first)"
    assert [c.label for c in section.columns] == [
        "Item",
        "Kind",
        "Id",
        "Last reviewed",
        "Age (days)",
    ]
    assert stale_rows(report) == [
        ("Test Wing Sauce", "component", "test-wing-sauce", "never", None),
        ("Test Buffalo Sliders", "recipe", "test-buffalo-sliders", "2025-01-01", 634),
        ("Test Citrus Wings", "recipe", "test-citrus-wings", "2025-09-26", 366),
    ]
    text = render_markdown(report)
    assert "| Test Wing Sauce | component | test-wing-sauce | never |  |" in text


def test_stale_reviews_none_due(fixture_book: Project) -> None:
    section = build_report(fixture_book).section("stale-reviews")
    assert section.title == "Published items not reviewed in 365 days (stalest first)"
    assert section.rows == ()
    assert section.empty == (
        "Every published recipe and component was reviewed in the last 365 days."
    )


def test_stale_reviews_use_threshold_date(fixture_book: Project) -> None:
    report = build_report(fixture_book, Thresholds(today=date(2027, 9, 2)))
    assert report.thresholds.today == date(2027, 9, 2)
    assert [r["id"] for r in rows(report, "stale-reviews")] == [
        "test-buffalo-sliders",
        "test-citrus-wings",
        "test-blue-cheese-dip",
        "test-cajun-seasoning",
        "test-wing-sauce",
    ]
    assert {r["age_days"] for r in rows(report, "stale-reviews")} == {366}


def test_stale_reviews_off(fixture_book: Project) -> None:
    book = fixture_book.content_root / "data/book.yml"
    text = book.read_text(encoding="utf-8")
    assert "review_max_age_days: 365" in text
    book.write_text(
        text.replace("review_max_age_days: 365", "review_max_age_days: null"), encoding="utf-8"
    )
    set_reviewed(fixture_book, SAUCE, None)
    section = build_report(fixture_book).section("stale-reviews")
    assert section.title == "Stale reviews"
    assert section.rows == ()
    assert section.empty == "Review age check is off: set review_max_age_days in data/book.yml."
