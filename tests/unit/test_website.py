"""Website generation reuses content without changing print output."""

import html
import json
import re
from pathlib import Path

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
        assert '<div class="print-bar" hidden' in page, name
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


PRINT_WITH = (
    '<label class="print-with" hidden><input type="checkbox" name="print-with"> '
    "Include homemade components</label>"
)

SHOP = (
    '<span class="shop-actions" hidden><span class="shop-label">Shopping list</span>'
    '<button type="button" class="shop-button" data-shop="txt">Download .txt</button>'
    '<button type="button" class="shop-button" data-shop="csv">Download .csv</button>'
    '<button type="button" class="shop-button" data-shop="copy">Copy</button>'
    '<span class="shop-status" aria-live="polite"></span></span>'
)


def test_recipe_and_component_print_bars_offer_a_shopping_list(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    sliders = (site / "recipe-test-buffalo-sliders.qmd").read_text()
    # Hidden until shop.js runs, after the component option inside the recipe's bar.
    assert f"{PRINT_WITH}{SHOP}</div>" in sliders
    sauce = (site / "component-test-wing-sauce.qmd").read_text()
    assert f'<button type="button" class="print-button">Print</button>{SHOP}</div>' in sauce
    # Page-level bars on menu and division pages print the page only.
    for name in ("menus-fast-day-1.qmd", "division-afc-east.qmd"):
        page = (site / name).read_text()
        assert page.count('class="shop-actions"') == page.count("print-bar print-menu"), name


def test_shop_script_ships_after_print_script(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    assert (site / "shop.js").read_text().startswith("// Shopping list on the website:")
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    assert "shop.js" in config["project"]["resources"]
    scripts = config["format"]["html"]["include-after-body"]["text"]
    assert scripts.index('<script src="print.js"></script>') < scripts.index(
        '<script src="shop.js"></script>'
    )


def test_recipe_print_bar_lists_its_component_pages_in_order(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    wings = (site / "recipe-test-citrus-wings.qmd").read_text()
    # The wing sauce uses the Cajun seasoning, so both print, in order of appearance.
    assert (
        '<div class="print-bar" hidden data-print-pages='
        '"component-test-wing-sauce.html component-test-cajun-seasoning.html">'
    ) in wings
    assert f'<button type="button" class="print-button">Print</button>{PRINT_WITH}' in wings
    # Component pages, and recipes without components, offer no extra pages.
    sauce = (site / "component-test-wing-sauce.qmd").read_text()
    assert "data-print-pages" not in sauce
    assert "print-with" not in sauce


def test_component_pages_print_once_after_first_use(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    recipe = fixture_book.recipes_dir / "afc/east/dolphins/test-citrus-wings.md"
    recipe.write_text(
        recipe.read_text().replace(
            "{{component:test-wing-sauce}}\n",
            "{{component:test-wing-sauce}}\n- 1 tsp seasoning {{component:test-cajun-seasoning}}\n",
        )
    )
    site = build_website(fixture_book, render=False).document.parent
    wings = (site / "recipe-test-citrus-wings.qmd").read_text()
    assert (
        'data-print-pages="component-test-wing-sauce.html component-test-cajun-seasoning.html"'
    ) in wings


def test_recipe_without_components_has_no_print_pages(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    recipe = fixture_book.recipes_dir / "afc/east/dolphins/test-citrus-wings.md"
    recipe.write_text(
        recipe.read_text().replace(
            "- 1 cup wing sauce {{component:test-wing-sauce}}", "- 1 cup wing sauce"
        )
    )
    site = build_website(fixture_book, render=False).document.parent
    wings = (site / "recipe-test-citrus-wings.qmd").read_text()
    assert '<div class="print-bar" hidden><button' in wings
    assert "data-print-pages" not in wings
    assert "print-with" not in wings


def test_print_pages_skip_components_left_out_of_the_book(
    fixture_book: Project, tmp_path: Path
) -> None:
    from nfl_book.digital import prepare_pages
    from nfl_book.website import _add_print_pages

    pages, _, _, model = prepare_pages(fixture_book, tmp_path / "site", web=True)
    # Validation stops published content referencing drafts, so drop one by hand.
    model.components = [c for c in model.components if c.id != "test-cajun-seasoning"]
    _add_print_pages(model, pages)
    wings = next(p for p in pages if p.slug == "recipe-test-citrus-wings")
    assert wings.context["print_pages"] == ["component-test-wing-sauce.html"]


def test_recipe_print_pages_exist_in_the_site_and_print_js_ships(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    wings = (site / "recipe-test-citrus-wings.qmd").read_text()
    match = re.search(r'data-print-pages="([^"]+)"', wings)
    assert match is not None
    pages = match.group(1).split()
    assert pages
    for page in pages:
        # Every page print.js fetches is a page of the generated site.
        assert (site / page.replace(".html", ".qmd")).is_file(), page
    # Hidden until print.js decides the site is served over http(s).
    assert '<label class="print-with" hidden>' in wings
    script = (site / "print.js").read_text()
    assert "pageList" in script and "printBundle" in script


MENU_PAGES = {
    "menus-fast-day-1.qmd": "## Test Quick Kickoff",
    "division-afc-east.qmd": "## Test AFC East Dish-Off",
}
MENU_BAR = (
    '<div class="print-bar print-menu" hidden data-print-pages='
    '"recipe-test-buffalo-sliders.html recipe-test-citrus-wings.html" data-print-components='
    '"component-test-blue-cheese-dip.html component-test-wing-sauce.html '
    'component-test-cajun-seasoning.html"><button type="button" class="print-button">'
    f"Print menu + recipes</button>{PRINT_WITH}{SHOP}</div>"
)


def test_menu_cards_carry_their_recipe_and_component_pages(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    for name, heading in MENU_PAGES.items():
        page = (site / name).read_text()
        # Recipes in menu order, then each component they use once, in order of first use.
        assert MENU_BAR in page, name
        card = page.index("::: {.menu-card}")
        assert card < page.index(heading) < page.index(MENU_BAR), name
        # The page's own Print button is unchanged.
        assert (
            '<div class="print-bar" hidden><button type="button" class="print-button">'
            "Print</button></div>"
        ) in page, name


def test_menu_print_pages_exist_in_the_site(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    for name in MENU_PAGES:
        page = (site / name).read_text()
        found = re.findall(r'data-print-(?:pages|components)="([^"]+)"', page)
        assert len(found) == 2, name
        for listed in found:
            for target in listed.split():
                assert (site / target.replace(".html", ".qmd")).is_file(), (name, target)


def test_menu_without_components_offers_no_component_option(fixture_book: Project) -> None:
    from nfl_book.website import build_website

    for relative, line in (
        (
            "afc/east/bills/test-buffalo-sliders.md",
            "- 1/2 cup blue cheese dip {{component:test-blue-cheese-dip}}",
        ),
        (
            "afc/east/dolphins/test-citrus-wings.md",
            "- 1 cup wing sauce {{component:test-wing-sauce}}",
        ),
    ):
        recipe = fixture_book.recipes_dir / relative
        text = recipe.read_text()
        assert line in text
        # A quick option only makes sense for a component the recipe still uses.
        text = text.replace(
            "quick_options:\n  test-blue-cheese-dip: "
            "Any chunky store-bought blue cheese dressing\n",
            "",
        )
        recipe.write_text(text.replace(line, line.split(" {{")[0]))
    site = build_website(fixture_book, render=False).document.parent
    division = (site / "division-afc-east.qmd").read_text()
    assert (
        '<div class="print-bar print-menu" hidden data-print-pages='
        '"recipe-test-buffalo-sliders.html recipe-test-citrus-wings.html"><button'
    ) in division
    assert "data-print-components" not in division
    assert "print-with" not in division


def test_browse_page_lists_every_card_and_hides_filters_until_scripted(
    fixture_book: Project,
) -> None:
    from nfl_book.website import build_website

    site = build_website(fixture_book, render=False).document.parent
    browse = (site / "browse.qmd").read_text()
    assert '<span id="section-browse"></span>' in browse
    assert "# Browse recipes" in browse
    assert '<form class="finder-filters" hidden aria-label="Filter recipes">' in browse
    assert '<div class="finder" data-total="2">' in browse
    assert '<p class="finder-status" aria-live="polite">2 recipes</p>' in browse
    cards = re.findall(r'<li class="finder-card" data-id="([^"]+)" data-facets="([^"]+)">', browse)
    assert [card[0] for card in cards] == ["test-buffalo-sliders", "test-citrus-wings"]
    facets = json.loads(html.unescape(cards[0][1]))
    assert facets["team"] == ["bills"] and facets["course"] == ["appetizers"]
    assert '<a href="recipe-test-buffalo-sliders.html">' in browse
    assert '<span class="finder-team">Buffalo Bills · Appetizer</span>' in browse
    assert '<span class="finder-photo-empty" aria-hidden="true"></span>' in browse
    assert 'name="team" value="dolphins"> Miami Dolphins' in browse
    assert "jets" not in browse
    assert "test-draft-nachos" not in browse
    assert browse.count('<fieldset data-facet="') == 7
    assert '<p class="finder-empty" hidden>' in browse
    assert '<script src="browse.js"></script>' in browse
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    sidebar = config["website"]["sidebar"]["contents"]
    assert sidebar[:3] == [
        {"text": "Start here", "href": "index.qmd"},
        {"text": "All recipes", "href": "contents.qmd"},
        {"text": "Browse recipes", "href": "browse.qmd"},
    ]


def test_browse_page_is_website_only(fixture_book: Project) -> None:
    pipeline.build(fixture_book, pdf=False)
    built = "\n".join(
        p.read_text()
        for p in fixture_book.book_build_dir.rglob("*")
        if p.suffix in {".qmd", ".tex"}
    )
    assert "Browse recipes" not in built
    assert "finder-card" not in built
