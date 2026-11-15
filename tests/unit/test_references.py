import pytest

from nfl_book.pipeline import load
from nfl_book.project import Project
from nfl_book.references import (
    LABEL_PREFIXES,
    Address,
    IndexPage,
    Item,
    KindSection,
    Placed,
    SectionPage,
    address,
    find_markers,
    menu_page_slug,
    parse_ingredient,
    parse_ingredients,
)
from nfl_book.resolve import BookModel, resolve


def test_plain_ingredient() -> None:
    item, problems = parse_ingredient("2 cups flour")
    assert problems == []
    assert item is not None
    assert item.text == "2 cups flour"
    assert item.component is None


def test_marker_is_stripped_from_display_text() -> None:
    item, problems = parse_ingredient("1/2 cup dip {{component:blue-cheese-dip}}")
    assert problems == []
    assert item is not None
    assert item.text == "1/2 cup dip"
    assert item.component == "blue-cheese-dip"


def test_marker_tolerates_inner_whitespace() -> None:
    item, _ = parse_ingredient("sauce {{ component : wing-sauce }}")
    assert item is not None and item.component == "wing-sauce"


def test_malformed_marker_is_rejected() -> None:
    item, problems = parse_ingredient("dip {{componet:blue-cheese-dip}}")
    assert item is None
    assert "malformed marker" in problems[0]


def test_two_markers_on_one_line_are_rejected() -> None:
    _, problems = parse_ingredient("{{component:a}} and {{component:b}}")
    assert any("only one component reference" in p for p in problems)


def test_marker_alone_needs_text() -> None:
    _, problems = parse_ingredient("{{component:a}}")
    assert any("needs text" in p for p in problems)


def test_invalid_component_id() -> None:
    _, problems = parse_ingredient("dip {{component:Blue_Cheese}}")
    assert any("invalid component id" in p for p in problems)


def test_groups() -> None:
    groups, problems = parse_ingredients(
        "- salt\n\n### Sauce\n\n- butter\n- hot sauce {{component:wing-sauce}}\n"
    )
    assert problems == []
    assert [g.heading for g in groups] == [None, "Sauce"]
    assert groups[1].items[1].component == "wing-sauce"


def test_non_bullet_line_is_reported_with_line_number() -> None:
    _, problems = parse_ingredients("- salt\nsome prose\n")
    assert problems == ["Ingredients line 2: expected '- item' or '### Group', got 'some prose'"]


def test_empty_group_and_empty_section() -> None:
    _, problems = parse_ingredients("### Empty\n")
    assert any("has no items" in p for p in problems)
    _, problems = parse_ingredients("")
    assert problems == ["Ingredients section has no items"]


def test_find_markers_ignores_single_braces() -> None:
    assert find_markers("use { } and $ freely") == []
    assert find_markers("see {{component:x}}") == ["{{component:x}}"]


def test_amounts_are_located_in_display_text() -> None:
    item, problems = parse_ingredient("1 1/2 cups dip {{component:blue-cheese-dip}}")
    assert problems == []
    assert item is not None
    assert [item.text[a.start : a.end] for a in item.amounts] == ["1 1/2 cups"]


def test_no_scale_marker_is_stripped_and_disables_scaling() -> None:
    item, problems = parse_ingredient("2 quarts oil for frying {{no-scale}}")
    assert problems == []
    assert item is not None
    assert item.text == "2 quarts oil for frying"
    assert item.amounts == ()


def test_no_scale_marker_combines_with_component_marker() -> None:
    item, problems = parse_ingredient("1 cup sauce {{no-scale}} {{component:wing-sauce}}")
    assert problems == []
    assert item is not None
    assert (item.text, item.component, item.amounts) == ("1 cup sauce", "wing-sauce", ())


def test_no_scale_marker_needs_an_amount() -> None:
    _, problems = parse_ingredient("Salt, to taste {{no-scale}}")
    assert any("only needed on a line with an amount" in p for p in problems)


def test_unreadable_amount_suggests_no_scale() -> None:
    item, problems = parse_ingredient("500g flour")
    assert item is None
    assert "space between the amount and unit" in problems[0]
    assert "{{no-scale}}" in problems[0]
    item, problems = parse_ingredient("500g flour {{no-scale}}")
    assert problems == []


# ---------------------------------------------------------------------------- addresses
BASE = "https://example.com/cookbook"
EDITION = f"{BASE}/v1.2.3/"


@pytest.fixture
def model(fixture_book: Project) -> BookModel:
    loaded = load(fixture_book)
    return resolve(loaded.settings, loaded.content, loaded.shortlinks.links)


def _consistent(where: Address) -> None:
    """The page fields name one page, and the HTML id is the label as a fragment."""
    assert where.page_source == f"{where.slug}.qmd"
    assert where.page_url == f"{where.slug}.html"
    assert where.html_id == where.label.replace(":", "-")
    assert ":" not in where.html_id
    assert where.label.startswith(LABEL_PREFIXES)
    if where.end_label:
        assert where.end_label == f"{where.label}:end"


def test_every_kind_has_a_consistent_address(model: BookModel) -> None:
    section = model.divisions[0]
    team = section.teams[0].team
    group = model.menu_groups[0]
    menu = group.menus[0]
    page = menu_page_slug(group.menu_type.id, 1)
    items: dict[str, Item] = {
        "recipe": model.recipes[0],
        "component": model.components[0],
        "division": section.division,
        "dish-off": section.dishoffs[0],
        "team": Placed(team, address(section.division).slug),
        "menu": Placed(menu, page),
        "section": SectionPage("contents"),
        "index": IndexPage(model.indexes[0].definition.id),
        "kind": KindSection(model.components[0].kind.id),
    }
    assert not {"recipe", "component", "division", "menu", "dish-off", "team", "section"} - set(
        items
    )
    for kind, item in items.items():
        where = address(item, edition=EDITION)
        assert where.kind == kind
        _consistent(where)

    recipe = address(items["recipe"])
    assert (recipe.label, recipe.slug) == (
        f"recipe:{model.recipes[0].id}",
        f"recipe-{model.recipes[0].id}",
    )
    assert recipe.end_label == f"{recipe.label}:end"
    assert address(items["component"]).end_label is None
    assert address(items["division"]).slug == f"division-{section.division.key}"


def test_anchors_live_on_the_page_that_holds_them(model: BookModel) -> None:
    section = model.divisions[0]
    division = address(section.division, edition=EDITION)
    team = address(Placed(section.teams[0].team, division.slug), edition=EDITION)
    dish_off = address(section.dishoffs[0], edition=EDITION)
    for anchored in (team, dish_off):
        assert (anchored.slug, anchored.page_source, anchored.page_url) == (
            division.slug,
            division.page_source,
            division.page_url,
        )
        assert anchored.edition_url == f"{EDITION}{division.page_url}#{anchored.html_id}"
    assert division.edition_url == f"{EDITION}{division.page_url}"
    assert team.label != division.label


def test_draft_recipe_has_no_edition_url(fixture_book: Project) -> None:
    loaded = load(fixture_book)
    recipes = {r.id: r for r in loaded.content.recipes}
    draft = recipes["test-draft-nachos"]
    published = recipes["test-citrus-wings"]
    assert address(draft, edition=EDITION).edition_url is None
    assert address(published, edition=EDITION).edition_url == f"{EDITION}recipe-{published.id}.html"
    assert address(published).edition_url is None  # no website_url configured


def test_component_kind_sections_are_not_on_the_website() -> None:
    where = address(KindSection("sauces"), edition=EDITION)
    assert where.label == "kind:sauces"
    assert where.html_id == "kind-sauces"
    assert where.edition_url is None
