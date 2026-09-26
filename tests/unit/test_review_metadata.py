"""Review metadata is validated, retained, and excluded from print output."""

from datetime import date
from pathlib import Path

import pytest

from nfl_book import pipeline
from nfl_book.config import load_settings
from nfl_book.discovery import discover
from nfl_book.errors import Diagnostics
from nfl_book.project import Project


def _recipe(project: Project) -> Path:
    return project.content_root / "recipes/afc/east/bills/test-buffalo-sliders.md"


@pytest.mark.parametrize("value", ["2026-09-26", "'2026-09-26'"])
def test_review_date_and_notes_are_loaded(fixture_book: Project, value: str) -> None:
    path = _recipe(fixture_book)
    path.write_text(
        path.read_text().replace(
            "status: published",
            f"status: published\nlast_reviewed_at: {value}\n"
            "last_reviewed_notes: 'Findings pending; report: docs/reviews/test.md'",
        )
    )
    diags = Diagnostics()
    content = discover(fixture_book, load_settings(fixture_book), diags)
    assert not diags.errors
    recipe = next(r for r in content.recipes if r.id == "test-buffalo-sliders")
    assert recipe.meta.last_reviewed_at == date(2026, 9, 26)
    assert recipe.meta.last_reviewed_notes == "Findings pending; report: docs/reviews/test.md"


def test_invalid_review_date_names_source(fixture_book: Project) -> None:
    path = _recipe(fixture_book)
    path.write_text(
        path.read_text().replace(
            "status: published", "status: published\nlast_reviewed_at: not-a-date"
        )
    )
    diags = Diagnostics()
    discover(fixture_book, load_settings(fixture_book), diags)
    assert any(d.path == path and "last_reviewed_at" in d.message for d in diags.errors)


def test_review_metadata_does_not_change_rendered_book(fixture_book: Project) -> None:
    pipeline.build(fixture_book, pdf=False)
    folder = fixture_book.book_build_dir
    before = {p.name: p.read_bytes() for p in (folder / "pages").glob("*.qmd")}
    path = _recipe(fixture_book)
    path.write_text(
        path.read_text().replace(
            "status: published",
            "status: published\nlast_reviewed_at: 2026-09-26\n"
            "last_reviewed_notes: PRIVATE_REVIEW_SENTINEL",
        )
    )
    pipeline.build(fixture_book, pdf=False)
    after = {p.name: p.read_bytes() for p in (folder / "pages").glob("*.qmd")}
    assert before == after
    assert b"PRIVATE_REVIEW_SENTINEL" not in (folder / "manifest.json").read_bytes()
