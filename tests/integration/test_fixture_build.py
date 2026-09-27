"""End-to-end proof on the synthetic fixture book.

The QMD half always runs. The PDF half needs Quarto + TinyTeX and is skipped
when they are not installed.
"""

from __future__ import annotations

import json
import re
import shutil

import pytest

from nfl_book import pipeline
from nfl_book.project import Project
from nfl_book.qr import qr_png


def pages(project: Project) -> dict[str, str]:
    build_dir = project.book_build_dir
    return {
        p.name: p.read_text(encoding="utf-8") for p in sorted((build_dir / "pages").glob("*.qmd"))
    }


def page(project: Project, suffix: str) -> str:
    matches = [text for name, text in pages(project).items() if name.endswith(f"-{suffix}.qmd")]
    assert len(matches) == 1, f"expected one page ending in {suffix}"
    return matches[0]


@pytest.fixture
def built(fixture_book: Project) -> Project:
    result = pipeline.build(fixture_book, pdf=False)
    assert result.document.is_file()
    assert result.pdf is None
    assert result.diagnostics.ok
    return fixture_book


def test_recipe_page_marks_components(built: Project) -> None:
    wings = page(built, "recipe-test-citrus-wings")
    assert r"\QMark{}\ComponentRef{component:test-wing-sauce}" in wings
    assert r"\begin{QuickOptionsCard}" in wings
    assert r"\QuickOption{component:test-wing-sauce}" in wings
    assert r"\BookEnd{recipe:test-citrus-wings:end}" in wings


def test_drafts_are_excluded(built: Project) -> None:
    everything = "\n".join(pages(built).values())
    assert "test-draft-nachos" not in everything
    assert "test-draft-side" not in everything


def test_transitive_component_page_is_included(built: Project) -> None:
    seasoning = page(built, "component-test-cajun-seasoning")
    # Used only through the wing sauce, but still credited to the wings.
    assert "recipe:test-citrus-wings" in seasoning


def test_menus_and_dishoffs(built: Project) -> None:
    division = page(built, "division-afc-east")
    assert r"\DishOffRecipe{recipe:test-buffalo-sliders}" in division
    assert "Test AFC East Dish-Off" in division
    assert "Test Quick Kickoff" in page(built, "menus-fast-day-1")


def test_no_page_numbers_in_source(built: Project) -> None:
    """Every cross-reference is a label; numbers are LaTeX's job."""
    everything = "\n".join(pages(built).values())
    assert r"\BookPageRef{recipe:test-citrus-wings}" in everything
    assert "p. " not in everything


def test_manifest_lists_every_anchor(built: Project) -> None:
    manifest = json.loads((built.book_build_dir / "manifest.json").read_text(encoding="utf-8"))
    anchors = {a for p in manifest["pages"] for a in p["anchors"]}
    assert {
        "section:contents",
        "division:afc-east",
        "recipe:test-buffalo-sliders",
        "recipe:test-citrus-wings:end",
        "component:test-cajun-seasoning",
        "menu:test-quick-kickoff",
    } <= anchors
    assert not any("draft" in a for a in anchors)
    spans = [tuple(s) for p in manifest["pages"] for s in p["spans"]]
    assert ("recipe:test-citrus-wings", "recipe:test-citrus-wings:end") in spans
    assert ("menu:test-quick-kickoff", "menu:test-quick-kickoff:end") in spans
    assert ("division:afc-east", "division:afc-east:end") in spans
    assert {"menu:test-quick-kickoff:end", "division:afc-east:end"} <= anchors


def test_menu_and_division_pages_mark_their_end(built: Project) -> None:
    menu = page(built, "menus-fast-day-1")
    end = r"\BookEnd{menu:test-quick-kickoff:end}"
    assert end in menu
    # Inside the last card, so a card that runs over carries the anchor with it.
    assert menu.index(end) < menu.rindex(r"\end{GameDayMenuCard}")
    division = page(built, "division-afc-east")
    end = r"\BookEnd{division:afc-east:end}"
    assert end in division
    assert division.index(end) < division.rindex(r"\end{DivisionDishOffCard}")


def test_menu_page_span_runs_from_first_to_last_card(fixture_book: Project) -> None:
    menus = fixture_book.content_root / "menus/game-day/fast-day"
    second = (menus / "test-quick-kickoff.yml").read_text(encoding="utf-8")
    second = second.replace("test-quick-kickoff", "test-second-kickoff")
    (menus / "test-second-kickoff.yml").write_text(second, encoding="utf-8")
    pipeline.build(fixture_book, pdf=False)
    manifest = json.loads(
        (fixture_book.book_build_dir / "manifest.json").read_text(encoding="utf-8")
    )
    spans = [tuple(s) for p in manifest["pages"] for s in p["spans"]]
    menu_spans = [s for s in spans if s[0].startswith("menu:")]
    assert len(menu_spans) == 1
    first, last = menu_spans[0]
    assert {first, last.removesuffix(":end")} == {
        "menu:test-quick-kickoff",
        "menu:test-second-kickoff",
    }
    assert last.endswith(":end")
    menu = page(fixture_book, "menus-fast-day-1")
    assert menu.count(r"\BookEnd{") == 1
    assert rf"\BookEnd{{{last}}}" in menu


def test_division_without_dishoffs_marks_its_end_after_the_teams(fixture_book: Project) -> None:
    (fixture_book.content_root / "menus/divisions/afc/east/test-afc-east-dish-off.yml").unlink()
    pipeline.build(fixture_book, pdf=False)
    division = page(fixture_book, "division-afc-east")
    assert "DivisionDishOffCard" not in division
    assert division.rstrip().endswith("\\BookEnd{division:afc-east:end}\n```")


def test_build_is_deterministic(fixture_book: Project) -> None:
    pipeline.build(fixture_book, pdf=False)
    first = pages(fixture_book)
    qr = {p.name: p.read_bytes() for p in (fixture_book.generated_dir / "qr").glob("*.png")}
    pipeline.build(fixture_book, pdf=False)
    assert pages(fixture_book) == first
    assert {p.name: p.read_bytes() for p in (fixture_book.generated_dir / "qr").glob("*.png")} == qr
    assert len(qr) == 5  # every published item, sourced or not


def test_qr_codes_encode_full_source_url_without_website_url(fixture_book: Project) -> None:
    book = fixture_book.content_root / "data/book.yml"
    book.write_text(re.sub(r"(?m)^website_url:.*$", "", book.read_text()))
    pipeline.build(fixture_book, pdf=False)
    png = (fixture_book.generated_dir / "qr" / "recipe-test-citrus-wings.png").read_bytes()
    assert png == qr_png("https://example.com/recipes/test-citrus-wings")
    assert png != qr_png("https://example.org/s/wings")
    # The printed link text stays the short URL.
    assert "example.org/s/wings" in page(fixture_book, "test-citrus-wings")


@pytest.mark.pdf
@pytest.mark.skipif(shutil.which("quarto") is None, reason="Quarto is not installed")
def test_fixture_pdf(fixture_book: Project) -> None:
    result = pipeline.build(fixture_book, pdf=True, strict=True)
    assert result.pdf is not None and result.pdf.is_file()
    assert result.diagnostics.ok
    pagemap = json.loads(fixture_book.pagemap_file.read_text(encoding="utf-8"))
    assert "recipe:test-citrus-wings" in pagemap


def test_shortcuts_follow_cooking_instructions(built: Project) -> None:
    wings = page(built, "recipe-test-citrus-wings")
    assert wings.index(r"\end{RecipeInstructions}") < wings.index(r"\begin{QuickOptionsCard}")
    component = page(built, "component-test-wing-sauce")
    assert component.index(r"\end{RecipeInstructions}") < component.index(r"\begin{BuyItCard}")
