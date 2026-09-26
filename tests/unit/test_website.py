"""Website generation reuses content without changing print output."""

import pytest
from typer.testing import CliRunner

from nfl_book import pipeline
from nfl_book.cli import app
from nfl_book.project import Project


def test_website_cli_generates_independent_sources(fixture_book: Project) -> None:
    pipeline.build(fixture_book, pdf=False)
    print_before = {
        p.relative_to(fixture_book.book_build_dir): p.read_bytes()
        for p in fixture_book.book_build_dir.rglob("*")
        if p.is_file()
    }
    source_before = {p: p.read_bytes() for p in fixture_book.content_root.rglob("*.md")}
    result = CliRunner().invoke(
        app,
        [
            "--root",
            str(fixture_book.root),
            "--content",
            str(fixture_book.content_root),
            "--generated",
            str(fixture_book.generated_dir),
            "--dist",
            str(fixture_book.dist_dir),
            "website",
            "--no-render",
        ],
    )
    assert result.exit_code == 0, result.output
    folder = fixture_book.generated_dir / "site"
    pages = {p.name: p.read_text() for p in folder.glob("*.qmd")}
    assert "index.qmd" in pages
    wings = pages["recipe-test-citrus-wings.qmd"]
    assert "component-test-wing-sauce.qmd#component-test-wing-sauce" in wings
    assert "example.org/s/wings" in wings
    assert "Quick options" in wings
    assert "Test AFC East Dish-Off" in pages["division-afc-east.qmd"]
    assert "Test Quick Kickoff" in pages["menus-fast-day-1.qmd"]
    text = "\n".join(pages.values())
    assert "test-draft-nachos" not in text
    assert "test-draft-side" not in text
    assert "last_reviewed" not in text
    assert "{=latex}" not in text
    assert (
        "recipe-test-citrus-wings.qmd#recipe-test-citrus-wings"
        in pages["component-test-cajun-seasoning.qmd"]
    )
    assert print_before == {
        p.relative_to(fixture_book.book_build_dir): p.read_bytes()
        for p in fixture_book.book_build_dir.rglob("*")
        if p.is_file()
    }
    assert all(p.read_bytes() == value for p, value in source_before.items())
    assert not (fixture_book.dist_dir / "site").exists()


def test_build_removes_stale_pages_and_keeps_review_notes_private(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    recipe = fixture_book.recipes_dir / "afc/east/bills/test-buffalo-sliders.md"
    recipe.write_text(
        recipe.read_text().replace(
            "status: published",
            "status: published\nlast_reviewed_notes: PRIVATE_EDITORIAL_SENTINEL",
        )
    )
    first = build_website(fixture_book, render=False)
    stale = first.document.parent / "recipe-retired.qmd"
    stale.write_text("retired")
    build_website(fixture_book, render=False)
    assert not stale.exists()
    assert all(
        "PRIVATE_EDITORIAL_SENTINEL" not in p.read_text()
        for p in first.document.parent.glob("*.qmd")
    )


def test_missing_quarto_preserves_previous_site(
    fixture_book: Project, monkeypatch: pytest.MonkeyPatch
) -> None:
    from nfl_book.errors import ValidationFailed
    from nfl_book.website import build_website

    site = fixture_book.dist_dir / "site"
    site.mkdir(parents=True)
    (site / "index.html").write_text("previous successful build")
    monkeypatch.setattr("nfl_book.website.shutil.which", lambda _: None)
    with pytest.raises(ValidationFailed) as raised:
        build_website(fixture_book)
    assert (site / "index.html").read_text() == "previous successful build"
    assert (
        raised.value.diagnostics.errors[0].path == fixture_book.generated_dir / "site/_quarto.yml"
    )


def test_recipe_descriptions_and_compact_menu_previews(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    pipeline.build(fixture_book, pdf=False)
    before = {p.name: p.read_bytes() for p in (fixture_book.book_build_dir / "pages").glob("*.qmd")}
    recipe = fixture_book.recipes_dir / "afc/east/bills/test-buffalo-sliders.md"
    recipe.write_text(
        recipe.read_text().replace(
            "status: published", 'status: published\ndescription: "Small rolls with beef & cheese."'
        )
    )
    site = build_website(fixture_book, render=False).document.parent
    division = (site / "division-afc-east.qmd").read_text()
    assert "Small rolls with beef &amp; cheese." in division
    menus = (site / "game-day-menus.qmd").read_text()
    assert "menu-preview-card" in menus
    assert "Test Quick Kickoff" in menus
    assert "recipe-test-buffalo-sliders.qmd#recipe-test-buffalo-sliders" in menus
    assert "recipe-test-citrus-wings.qmd#recipe-test-citrus-wings" in menus
    assert "Small rolls with beef" not in menus  # previews stay compact
    pipeline.build(fixture_book, pdf=False)
    assert before == {
        p.name: p.read_bytes() for p in (fixture_book.book_build_dir / "pages").glob("*.qmd")
    }
