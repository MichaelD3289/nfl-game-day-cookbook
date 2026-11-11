"""The discovery presentation uses published synthetic content and existing tools."""

import re

import yaml

from nfl_book.project import Project
from nfl_book.qr import qr_png
from nfl_book.website import build_website


def test_home_exposes_published_recipes_courses_and_existing_tools(fixture_book: Project) -> None:
    site = build_website(fixture_book, render=False).document.parent
    home = (site / "index.qmd").read_text()
    assert "A little road trip." in home
    assert 'class="discovery-cards"' in home
    assert 'href="recipe-test-buffalo-sliders.html"' in home
    assert 'href="recipe-test-citrus-wings.html"' in home
    assert '<span class="finder-location">Buffalo, New York</span>' in home
    assert '<span class="finder-team">Buffalo Bills</span>' in home
    assert 'href="browse.html?course=appetizers"' in home
    assert 'href="menu-builder.qmd"' in home
    assert 'href="game-day-menus.qmd"' in home
    assert "test-draft" not in home
    assert not re.search(r'<img[^>]+src=""', home)


def test_cards_keep_city_team_and_course_distinct(fixture_book: Project) -> None:
    recipe = fixture_book.recipes_dir / "afc/east/bills/test-buffalo-sliders.md"
    recipe.write_text(
        recipe.read_text().replace(
            "course: appetizers", 'course: appetizers\nlocation: "Test City & Harbor, NY"'
        )
    )
    site = build_website(fixture_book, render=False).document.parent
    for name in ("browse.qmd", "index.qmd"):
        text = (site / name).read_text()
        assert '<span class="finder-location">Test City &amp; Harbor, NY</span>' in text
        assert '<span class="finder-team">Buffalo Bills</span>' in text
        assert 'class="finder-facts"' in text
    builder = (site / "menu-builder.qmd").read_text()
    assert '<span class="menu-dish-location">Test City &amp; Harbor, NY</span>' in builder
    assert '<span class="menu-dish-team">Buffalo Bills</span>' in builder


def test_home_uses_available_photos_and_has_an_empty_collection_fallback(
    fixture_book: Project, empty_book: Project
) -> None:
    recipe = fixture_book.recipes_dir / "afc/east/bills/test-buffalo-sliders.md"
    recipe.write_text(
        recipe.read_text().replace(
            "status: published",
            "status: published\nimage: test-photo.png\nphoto_credit: Synthetic fixture",
        )
    )
    (recipe.parent / "test-photo.png").write_bytes(qr_png("https://example.invalid/test-photo"))
    site = build_website(fixture_book, render=False).document.parent
    home = (site / "index.qmd").read_text()
    assert 'class="hero-photos single-photo"' in home
    assert 'src="assets/recipe-test-buffalo-sliders.webp"' in home
    assert 'alt="Test Buffalo Sliders"' in home
    assert 'loading="eager"' in home
    empty = build_website(empty_book, render=False).document.parent
    text = (empty / "index.qmd").read_text()
    assert "A little road trip." in text
    assert "<img" not in text
    assert 'href="browse.qmd"' in text


def test_navigation_preserves_search_team_indexes_and_downloads(fixture_book: Project) -> None:
    site = build_website(fixture_book, render=False).document.parent
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    website = config["website"]
    assert website["search"] == {"location": "navbar", "type": "overlay"}
    assert "sidebar" not in website
    links = str(website["navbar"])
    for target in (
        "browse.qmd",
        "game-day-menus.qmd",
        "menu-builder.qmd",
        "matchup.qmd",
        "contents.qmd",
        "division-afc-east.qmd",
        "index-course.qmd",
        "make-it-or-buy-it.qmd",
        "versions.qmd",
        "Download PDF",
        "Download EPUB",
    ):
        assert target in links


def test_curated_menu_can_open_its_dishes_in_existing_builder(fixture_book: Project) -> None:
    site = build_website(fixture_book, render=False).document.parent
    text = (site / "game-day-menus.qmd").read_text()
    assert 'href="menu-builder.html?r=test-buffalo-sliders,test-citrus-wings"' in text
    assert "Make it your own" in text
    assert "Buffalo Bills" in text
    assert "Miami Dolphins" in text
