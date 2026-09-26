from nfl_book.references import find_markers, parse_ingredient, parse_ingredients


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
