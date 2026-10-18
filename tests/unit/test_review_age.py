"""Published recipes and components whose review is missing or too old raise warnings."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from nfl_book.errors import Diagnostic, ValidationFailed
from nfl_book.pipeline import load, validate
from nfl_book.project import Project
from nfl_book.reviews import stale_reviews

SLIDERS = "recipes/afc/east/bills/test-buffalo-sliders.md"
NACHOS = "recipes/afc/east/jets/test-draft-nachos.md"
SAUCE = "components/sauces/test-wing-sauce.md"
FIXTURE_DATE = "last_reviewed_at: 2026-09-01\n"


def edit(project: Project, relative: str, old: str, new: str) -> Path:
    path = project.content_root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {relative}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return path


def set_limit(project: Project, line: str) -> Path:
    return edit(project, "data/book.yml", "review_max_age_days: 365\n", line)


def review_warnings(project: Project) -> list[Diagnostic]:
    diags = load(project).diagnostics
    assert diags.ok, [d.message for d in diags.errors]
    return [d for d in diags.warnings if d.code == "review"]


def test_old_recipe_review_warns(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, FIXTURE_DATE, "last_reviewed_at: 2025-01-01\n")
    diags = load(fixture_book).diagnostics
    warnings = [d for d in diags.warnings if d.code == "review"]
    assert len(warnings) == 1
    assert warnings[0].path == path
    assert "634 days" in warnings[0].message
    assert "365" in warnings[0].message
    assert diags.ok


def test_component_without_review_date_warns(fixture_book: Project) -> None:
    path = edit(fixture_book, SAUCE, FIXTURE_DATE, "")
    warnings = review_warnings(fixture_book)
    assert [d.path for d in warnings] == [path]
    assert "no last_reviewed_at" in warnings[0].message
    assert "published component" in warnings[0].message


def test_exactly_at_limit_is_fine(fixture_book: Project) -> None:
    edit(fixture_book, SLIDERS, FIXTURE_DATE, "last_reviewed_at: 2025-09-27\n")
    assert review_warnings(fixture_book) == []


def test_one_day_over_limit_warns(fixture_book: Project) -> None:
    edit(fixture_book, SLIDERS, FIXTURE_DATE, "last_reviewed_at: 2025-09-26\n")
    warnings = review_warnings(fixture_book)
    assert len(warnings) == 1
    assert "366 days" in warnings[0].message


def test_drafts_are_ignored(fixture_book: Project) -> None:
    text = (fixture_book.content_root / NACHOS).read_text(encoding="utf-8")
    assert "last_reviewed_at: 2020-01-01" in text
    assert review_warnings(fixture_book) == []


def test_future_review_date_warns(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, FIXTURE_DATE, "last_reviewed_at: 2026-10-01\n")
    warnings = review_warnings(fixture_book)
    assert [d.path for d in warnings] == [path]
    assert "2026-10-01 is after today (2026-09-27)" in warnings[0].message


@pytest.mark.parametrize("line", ["review_max_age_days: null\n", ""])
def test_check_is_off_without_a_limit(fixture_book: Project, line: str) -> None:
    set_limit(fixture_book, line)
    edit(fixture_book, SLIDERS, FIXTURE_DATE, "last_reviewed_at: 2020-01-01\n")
    edit(fixture_book, SAUCE, FIXTURE_DATE, "")
    assert review_warnings(fixture_book) == []


def test_invalid_limit_names_book_yml(fixture_book: Project) -> None:
    path = set_limit(fixture_book, "review_max_age_days: 0\n")
    with pytest.raises(ValidationFailed) as caught:
        load(fixture_book)
    assert any(
        d.path == path and "review_max_age_days" in d.message
        for d in caught.value.diagnostics.errors
    )


def test_stale_reviews_with_explicit_today(fixture_book: Project) -> None:
    content = load(fixture_book).content
    stale = stale_reviews(content.recipes, content.components, 365, today=date(2027, 9, 2))
    assert [(s.kind, s.item.id) for s in stale] == [
        ("recipe", "test-buffalo-sliders"),
        ("recipe", "test-citrus-wings"),
        ("component", "test-blue-cheese-dip"),
        ("component", "test-cajun-seasoning"),
        ("component", "test-wing-sauce"),
    ]
    assert {s.age_days for s in stale} == {366}
    assert {s.last_reviewed_at for s in stale} == {date(2026, 9, 1)}
    assert stale_reviews(content.recipes, content.components, 365, today=date(2027, 9, 1)) == []


def test_stale_reviews_lists_missing_then_oldest(fixture_book: Project) -> None:
    edit(fixture_book, SAUCE, FIXTURE_DATE, "")
    edit(fixture_book, SLIDERS, FIXTURE_DATE, "last_reviewed_at: 2024-01-01\n")
    content = load(fixture_book).content
    stale = stale_reviews(content.recipes, content.components, 365, today=date(2027, 9, 2))
    assert [s.item.id for s in stale][:2] == ["test-wing-sauce", "test-buffalo-sliders"]
    assert stale[0].age_days is None
    assert stale[0].last_reviewed_at is None


def test_path_filter_reports_only_matching_files(fixture_book: Project) -> None:
    sliders = edit(fixture_book, SLIDERS, FIXTURE_DATE, "last_reviewed_at: 2025-01-01\n")
    edit(fixture_book, SAUCE, FIXTURE_DATE, "")
    assert len(review_warnings(fixture_book)) == 2
    diags = validate(fixture_book, [sliders])
    assert [(d.code, d.path) for d in diags.warnings] == [("review", sliders)]
