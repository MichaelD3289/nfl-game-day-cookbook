from __future__ import annotations

import pytest

from nfl_book.config import Settings
from nfl_book.errors import BookError
from nfl_book.pipeline import load
from nfl_book.project import Project
from nfl_book.scaffold import new_component, new_recipe


def test_new_recipe_is_a_draft_in_the_team_directory(
    empty_book: Project, settings: Settings
) -> None:
    path = new_recipe(empty_book, settings, "packers", "brat-dip")
    assert path == empty_book.recipes_dir / "nfc/north/packers/brat-dip.md"
    text = path.read_text()
    assert "status: draft" in text
    assert "team:" not in text
    for key in ("main_ingredient:", "practical_time:", "cost:"):
        assert key in text


def test_scaffolded_files_parse(empty_book: Project, settings: Settings) -> None:
    new_recipe(empty_book, settings, "packers", "brat-dip")
    new_component(empty_book, settings, "sauces", "beer-cheese")
    diags = load(empty_book).diagnostics
    # drafts may hold TODO placeholders, but the structure itself must be valid
    assert not [
        d for d in diags.errors if d.code in {"parse", "structure", "ingredients", "location"}
    ]


def test_refuses_to_overwrite(empty_book: Project, settings: Settings) -> None:
    path = new_recipe(empty_book, settings, "packers", "brat-dip")
    path.write_text("hand edited")
    with pytest.raises(BookError, match="already"):
        new_recipe(empty_book, settings, "packers", "brat-dip")
    with pytest.raises(BookError, match="already used"):
        new_recipe(empty_book, settings, "bears", "brat-dip")
    assert path.read_text() == "hand edited"


def test_rejects_unknown_team_kind_and_bad_slug(empty_book: Project, settings: Settings) -> None:
    with pytest.raises(BookError, match="unknown team"):
        new_recipe(empty_book, settings, "cowboy", "x")
    with pytest.raises(BookError, match="unknown component kind"):
        new_component(empty_book, settings, "gravies", "x")
    with pytest.raises(BookError, match="invalid slug"):
        new_recipe(empty_book, settings, "packers", "Brat Dip")


def test_new_component_location(empty_book: Project, settings: Settings) -> None:
    path = new_component(empty_book, settings, "dips", "queso")
    assert path == empty_book.components_dir / "dips/queso.md"
    assert "status: draft" in path.read_text()
