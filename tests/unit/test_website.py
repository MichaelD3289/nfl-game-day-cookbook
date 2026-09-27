"""Website generation reuses content without changing print output."""

import html
import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml
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


def _describe(project: Project, relative: str, description: str) -> None:
    path = project.content_root / relative
    text = path.read_text()
    path.write_text(
        text.replace("status: published", f"status: published\ndescription: {description}", 1)
    )


def test_make_buy_cards_show_component_descriptions_and_recipes(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    _describe(fixture_book, "components/sauces/test-wing-sauce.md", '"Hot & tangy wing sauce."')
    site = build_website(fixture_book, render=False).document.parent
    make_buy = (site / "make-it-or-buy-it.qmd").read_text()
    card = make_buy[make_buy.index("Test Wing Sauce") :]
    card = card[: card.index("::: {.component-card}") if "::: {.component-card}" in card else None]
    assert '<p class="dish-description">Hot &amp; tangy wing sauce.</p>' in card
    assert (
        'class="used-in-chip" href="recipe-test-citrus-wings.qmd#recipe-test-citrus-wings"' in card
    )
    assert '<span class="used-in-team">Dolphins</span>' in card
    component = (site / "component-test-wing-sauce.qmd").read_text()
    assert '<p class="page-dek">Hot &amp; tangy wing sauce.</p>' in component
    # The description is for browsing on screen; the print booklet leaves it out.
    pipeline.build(fixture_book, pdf=False)
    pages = fixture_book.book_build_dir / "pages"
    assert not any("tangy wing sauce" in p.read_text() for p in pages.glob("*.qmd"))


def test_dish_entries_share_name_meta_and_description(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    _describe(fixture_book, "recipes/afc/east/bills/test-buffalo-sliders.md", '"Small rolls."')
    site = build_website(fixture_book, render=False).document.parent
    entry = (
        '<a class="dish-name" href="recipe-test-buffalo-sliders.qmd#recipe-test-buffalo-sliders">'
        "Test Buffalo Sliders</a> "
    )
    division = (site / "division-afc-east.qmd").read_text()
    # Team cards drop the team they are about; dish-offs mixing teams keep it.
    assert f'{entry}<span class="dish-meta">Appetizer</span>' in division
    assert f'{entry}<span class="dish-meta">Bills · Appetizer</span>' in division
    assert "::: {.dish-list}" in division
    menus = (site / "game-day-menus.qmd").read_text()
    assert '<span class="dish-meta">Bills · Appetizer</span>' in menus
    assert ".dish-list-compact" in menus
    recipe = (site / "recipe-test-buffalo-sliders.qmd").read_text()
    assert '<p class="page-dek">Small rolls.</p>' in recipe
    assert (
        '<ul class="recipe-facts"><li class="fact-yield"><span class="fact-name">Yield</span>'
        in recipe
    )


def _set_form_url(project: Project, value: str) -> Path:
    book = project.content_root / "data/book.yml"
    text = re.sub(r"(?m)^suggestion_form_url:.*$", "", book.read_text())
    book.write_text(f"{text.rstrip()}\nsuggestion_form_url: {value}\n")
    return book


def test_suggestion_prompts_link_to_prefilled_quick_templates(fixture_book: Project) -> None:
    from urllib.parse import parse_qs, urlsplit

    from nfl_book.website import build_website

    _set_form_url(fixture_book, "")
    site = build_website(fixture_book, render=False).document.parent
    wings = (site / "recipe-test-citrus-wings.qmd").read_text()
    href = re.search(r'class="suggest-github" href="([^"]+)"', wings)
    assert href is not None
    query = parse_qs(urlsplit(html.unescape(href.group(1))).query)
    assert query["template"] == ["suggest-edit.yml"]
    assert query["title"][0].startswith("Edit suggestion: Test Citrus Wings")
    assert "[recipe:test-citrus-wings]" in query["item"][0]
    assert query["page"][0].endswith("/test-citrus-wings.md")
    assert "Spot something to fix in this recipe?" in wings
    division = (site / "division-afc-east.qmd").read_text()
    assert "template=quick-recipe.yml" in division
    assert "template=quick-dish-off.yml" in division
    assert "template=quick-menu.yml" in (site / "game-day-menus.qmd").read_text()
    assert "template=quick-component.yml" in (site / "make-it-or-buy-it.qmd").read_text()
    assert "suggest-edit.yml" in (site / "component-test-wing-sauce.qmd").read_text()
    # Without a configured form only the GitHub path is offered.
    assert "suggest-open" not in wings
    assert not (site / "suggest.js").exists()
    assert "suggest.js" not in (site / "_quarto.yml").read_text()


def test_configured_form_adds_anonymous_button_and_script(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    endpoint = "https://script.google.com/macros/s/test-deployment/exec"
    _set_form_url(fixture_book, endpoint)
    site = build_website(fixture_book, render=False).document.parent
    wings = (site / "recipe-test-citrus-wings.qmd").read_text()
    assert f'class="suggest-open" data-endpoint="{endpoint}"' in wings
    fields = re.search(r'data-fields="([^"]+)"', wings)
    assert fields is not None
    assert json.loads(html.unescape(fields.group(1)))["item"].startswith("Test Citrus Wings")
    assert (site / "suggest.js").is_file()
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    assert "suggest.js" in config["project"]["resources"]
    assert "suggest.js" in config["format"]["html"]["include-after-body"]["text"]


def test_suggestion_form_url_must_be_https(fixture_book: Project) -> None:
    from nfl_book.errors import ValidationFailed
    from nfl_book.website import build_website

    book = _set_form_url(fixture_book, "http://x")
    with pytest.raises(ValidationFailed) as raised:
        build_website(fixture_book, render=False)
    assert raised.value.diagnostics.errors[0].path == book


def test_scalable_pages_mark_amounts_and_offer_controls(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    sliders = (site / "recipe-test-buffalo-sliders.qmd").read_text()
    assert '<span class="qty" data-q="1" data-unit="lb">1 lb</span> ground chicken' in sliders
    assert '<span class="qty" data-q="12">12</span> slider buns' in sliders
    assert (
        '<span class="qty" data-q="1/2" data-unit="cup">1/2 cup</span> blue cheese dip' in sliders
    )
    assert "- 2 cups oil for the griddle\n" in sliders  # {{no-scale}}
    assert "{{no-scale}}" not in sliders
    assert '<div class="scaler" data-servings="4" data-servings-max="6" hidden>' in sliders
    assert "(serves 4–6 as written)" in sliders
    assert 'data-factor="3/2"' in sliders
    assert '<script src="scale.js"></script>' in sliders
    assert 'class="q-mark" href="component-test-blue-cheese-dip.qmd' in sliders
    assert "data-carry-scale" in sliders
    # Components scale by multiplier only; recipes without servings do the same.
    sauce = (site / "component-test-wing-sauce.qmd").read_text()
    assert '<div class="scaler" hidden>' in sauce
    assert 'name="servings"' not in sauce
    assert (site / "scale.js").read_text().startswith("// Recipe scaling on the website.")
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    assert "scale.js" in config["project"]["resources"]


def test_scaling_leaves_print_pages_unchanged(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    pipeline.build(fixture_book, pdf=False)
    pages = fixture_book.book_build_dir / "pages"
    before = {p.name: p.read_bytes() for p in pages.glob("*.qmd")}
    text = "\n".join(p.decode() for p in before.values())
    assert "2 cups oil for the griddle" in text
    assert "no-scale" not in text
    assert "qty" not in text
    assert "scaler" not in text
    build_website(fixture_book, render=False)
    pipeline.build(fixture_book, pdf=False)
    assert before == {p.name: p.read_bytes() for p in pages.glob("*.qmd")}


def test_versions_page_has_marker_for_published_versions(fixture_book: Project) -> None:
    from nfl_book.site_archive import VERSIONS_MARKER
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    assert VERSIONS_MARKER in (site / "versions.qmd").read_text()
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    navbar = config["website"]["navbar"]["right"]
    assert {"text": "All versions", "href": "versions.qmd"} in navbar


def test_printable_pages_offer_a_print_button(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    printable = [
        "recipe-test-citrus-wings.qmd",
        "component-test-wing-sauce.qmd",
        "menus-fast-day-1.qmd",
        "division-afc-east.qmd",
    ]
    for name in printable:
        page = (site / name).read_text()
        # Hidden until print.js runs, so readers without JavaScript never see a dead button.
        assert '<div class="print-bar" hidden>' in page, name
        assert '<button type="button" class="print-button">Print</button>' in page, name
    for name in ("index.qmd", "contents.qmd", "game-day-menus.qmd", "versions.qmd"):
        assert "print-bar" not in (site / name).read_text(), name
    # The printout names the scale it was printed at.
    sliders = (site / "recipe-test-buffalo-sliders.qmd").read_text()
    assert '<p class="print-scale" hidden></p>' in sliders
    assert '<div class="scaler" data-servings="4" data-servings-max="6" hidden>' in sliders
    assert "print-scale" not in (site / "division-afc-east.qmd").read_text()
    assert (site / "print.js").read_text().startswith("// Print button on the website.")
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    assert "print.js" in config["project"]["resources"]
    assert "print.js" in config["format"]["html"]["include-after-body"]["text"]


def test_print_script_is_kept_alongside_suggestion_script(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    _set_form_url(fixture_book, "https://script.google.com/macros/s/test-deployment/exec")
    site = build_website(fixture_book, render=False).document.parent
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    scripts = config["format"]["html"]["include-after-body"]["text"]
    assert '<script src="print.js"></script>' in scripts
    assert '<script src="suggest.js"></script>' in scripts


def test_preview_builds_are_labelled_on_every_page(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    assert "include-before-body" not in config["format"]["html"]
    assert config["website"]["page-footer"]["right"].startswith("Edition ")

    site = build_website(fixture_book, render=False, preview="ui<polish> @ 1a2b3c4").document.parent
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    banner = config["format"]["html"]["include-before-body"]["text"]
    assert 'class="preview-banner"' in banner
    assert "ui&lt;polish&gt; @ 1a2b3c4" in banner
    assert config["website"]["page-footer"]["right"] == "Preview ui&lt;polish&gt; @ 1a2b3c4"


def test_source_is_one_named_link_with_the_short_address_for_paper(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    wings = (site / "recipe-test-citrus-wings.qmd").read_text()
    source = wings[wings.index("**Recipe source:**") :]
    source = source[: source.index("\n:::")]
    assert (
        '**Recipe source:** <a href="https://example.com/recipes/test-citrus-wings">example.com</a>'
        in source
    )
    # The address shows once, in the print view only (styled by .source-url).
    assert source.count('<span class="source-url">') == 1
    assert "<small>" not in source


def _json_ld(page: Path) -> tuple[dict[str, Any] | None, str]:
    """The page's schema.org JSON-LD (None without one) and its whole header include."""
    front = yaml.safe_load(page.read_text().split("---\n")[1])
    head = str(front.get("include-in-header", {}).get("text", ""))
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', head, re.DOTALL)
    return (json.loads(match.group(1)) if match else None), head


def _canonical(head: str) -> str | None:
    match = re.search(r'<link rel="canonical" href="([^"]+)">', head)
    return html.unescape(match.group(1)) if match else None


def test_recipe_pages_carry_schema_org_recipe_json_ld(fixture_book: Project) -> None:
    from nfl_book import __version__
    from nfl_book.config import load_settings
    from nfl_book.qr import qr_png
    from nfl_book.website import build_website

    recipe = fixture_book.recipes_dir / "afc/east/bills/test-buffalo-sliders.md"
    recipe.write_text(
        recipe.read_text()
        .replace("prep: 15 min", "prep: PT15M")
        .replace("cook: 20 min", "cook: 20 minutes")
        .replace(
            "status: published",
            "status: published\ndescription: Small chicken rolls with blue cheese.\n"
            "image: fixture.png\nphoto_credit: Synthetic fixture",
        )
    )
    (recipe.parent / "fixture.png").write_bytes(qr_png("https://example.com/synthetic-photo"))
    settings = load_settings(fixture_book)
    base = settings.book.website_url
    assert base
    edition = f"{base.rstrip('/')}/v{__version__}/"
    site = build_website(fixture_book, render=False).document.parent

    data, head = _json_ld(site / "recipe-test-buffalo-sliders.qmd")
    assert data is not None
    assert data["@context"] == "https://schema.org"
    assert data["@type"] == "Recipe"
    assert data["name"] == "Test Buffalo Sliders"
    assert data["description"] == "Small chicken rolls with blue cheese."
    assert data["recipeYield"] == "12 sliders"
    assert data["recipeCategory"] == settings.course("appetizers").label  # type: ignore[union-attr]
    assert data["recipeCuisine"] == "Buffalo, New York"
    assert (data["prepTime"], data["cookTime"], data["totalTime"]) == ("PT15M", "PT20M", "PT35M")
    assert "Poultry" in data["keywords"].split(", ")
    assert "Buffalo Bills" in data["keywords"].split(", ")
    assert data["recipeIngredient"] == [
        "1 lb ground chicken",
        "12 slider buns",
        "2 cups oil for the griddle",
        "1/2 cup blue cheese dip",
        "Celery sticks & carrot sticks (100% optional)",
    ]
    assert not any(
        marker in line
        for line in data["recipeIngredient"]
        for marker in ("{{", "component:", "no-scale")
    )
    assert data["recipeInstructions"] == [
        {"@type": "HowToStep", "text": "Form 12 patties and cook until done."},
        {"@type": "HowToStep", "text": "Spoon the dip over each slider and serve."},
    ]
    assert data["isBasedOn"] == "https://example.com/recipes/test-buffalo-sliders?ref=fixture&x=1"
    assert data["url"] == f"{edition}recipe-test-buffalo-sliders.html"
    assert data["image"] == f"{edition}assets/recipe-test-buffalo-sliders.webp"
    assert _canonical(head) == f"{base.rstrip('/')}/recipe-test-buffalo-sliders.html"
    assert "author" not in data
    assert "aggregateRating" not in data


def test_prose_times_and_missing_fields_are_left_out(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    recipe = fixture_book.recipes_dir / "afc/east/bills/test-buffalo-sliders.md"
    recipe.write_text(recipe.read_text().replace("prep: 15 min", "prep: 15 min (estimated)"))
    site = build_website(fixture_book, render=False).document.parent

    sliders, _ = _json_ld(site / "recipe-test-buffalo-sliders.qmd")
    assert sliders is not None
    assert "prepTime" not in sliders
    assert sliders["cookTime"] == "PT20M"
    assert "totalTime" not in sliders

    wings, head = _json_ld(site / "recipe-test-citrus-wings.qmd")
    assert wings is not None
    assert wings["recipeInstructions"] == [
        {"@type": "HowToStep", "text": "Bake the wings, then toss them in the sauce."}
    ]
    for key in ("image", "description", "prepTime", "cookTime", "totalTime"):
        assert key not in wings
    assert _canonical(head)

    for name in (
        "component-test-blue-cheese-dip.qmd",
        "division-afc-east.qmd",
        "game-day-menus.qmd",
        "menus-fast-day-1.qmd",
        "index.qmd",
    ):
        data, head = _json_ld(site / name)
        assert data is None and head == "", name
    assert not (site / "recipe-test-draft-nachos.qmd").exists()


def test_json_ld_without_website_url(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    book = fixture_book.content_root / "data/book.yml"
    book.write_text(re.sub(r"(?m)^website_url:.*$", "", book.read_text()))
    site = build_website(fixture_book, render=False).document.parent
    data, head = _json_ld(site / "recipe-test-buffalo-sliders.qmd")
    assert data is not None
    assert data["@type"] == "Recipe"
    assert "url" not in data
    assert "image" not in data
    assert _canonical(head) is None
