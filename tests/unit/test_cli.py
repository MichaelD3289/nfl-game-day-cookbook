"""CLI wiring: exit codes, messages and that every command honours the path options."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nfl_book import cli
from nfl_book.pipeline import load
from nfl_book.project import Project

runner = CliRunner()


@pytest.fixture(autouse=True)
def reset_state() -> Iterator[None]:
    cli.state = cli.State()
    yield
    cli.state = cli.State()


def invoke(project: Project, *args: str) -> tuple[int, str]:
    content = project.content_root
    result = runner.invoke(
        cli.app,
        [
            "--root",
            str(project.root),
            "--content",
            str(content),
            "--generated",
            str(content / "generated"),
            "--dist",
            str(content / "dist"),
            *args,
        ],
    )
    return result.exit_code, result.output


def test_validate_ok(fixture_book: Project) -> None:
    code, output = invoke(fixture_book, "validate")
    assert code == 0, output
    assert "OK" in output


def test_validate_failure_names_file(fixture_book: Project) -> None:
    path = fixture_book.content_root / "recipes/afc/east/bills/test-buffalo-sliders.md"
    path.write_text(path.read_text().replace("course:", "course_typo:"), encoding="utf-8")
    code, output = invoke(fixture_book, "validate")
    assert code == 1
    assert "test-buffalo-sliders.md" in output


def test_build_without_pdf(fixture_book: Project) -> None:
    code, output = invoke(fixture_book, "build", "--no-pdf")
    assert code == 0, output
    assert "QMD:" in output
    assert (fixture_book.content_root / "generated/book/book.qmd").is_file()


def test_preview_draft_recipe(fixture_book: Project) -> None:
    draft = fixture_book.content_root / "recipes/afc/east/jets/test-draft-nachos.md"
    code, output = invoke(fixture_book, "preview", str(draft), "--no-pdf")
    assert code == 0, output
    assert "QMD:" in output


def test_new_recipe_and_component(fixture_book: Project) -> None:
    code, output = invoke(fixture_book, "new", "recipe", "--team", "packers", "--slug", "brat-dip")
    assert code == 0, output
    assert (fixture_book.content_root / "recipes/nfc/north/packers/brat-dip.md").is_file()

    code, output = invoke(
        fixture_book, "new", "component", "--kind", "sauces", "--slug", "beer-cheese"
    )
    assert code == 0, output
    assert (fixture_book.content_root / "components/sauces/beer-cheese.md").is_file()

    code, output = invoke(fixture_book, "new", "recipe", "--team", "packers", "--slug", "brat-dip")
    assert code == 1


def test_clean(fixture_book: Project) -> None:
    assert invoke(fixture_book, "build", "--no-pdf")[0] == 0
    code, output = invoke(fixture_book, "clean")
    assert code == 0, output
    assert not (fixture_book.content_root / "generated").exists()


def test_production_skeleton_validates() -> None:
    """The committed (empty) production tree is always a valid book."""
    root = Path(__file__).resolve().parents[2]
    diags = load(Project.create(root)).diagnostics
    assert diags.ok, [d.message for d in diags.errors]
