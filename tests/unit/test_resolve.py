"""Publication rules: what reaches the book, and in what order."""

from __future__ import annotations

from nfl_book.pipeline import load
from nfl_book.project import Project
from nfl_book.resolve import BookModel, resolve


def model_for(project: Project) -> BookModel:
    loaded = load(project)
    assert loaded.diagnostics.ok, list(loaded.diagnostics)
    return resolve(loaded.settings, loaded.content, loaded.shortlinks.links)


def test_only_published_recipes(fixture_book: Project) -> None:
    ids = [r.id for r in model_for(fixture_book).recipes]
    assert ids == ["test-buffalo-sliders", "test-citrus-wings"]  # league order: bills, dolphins


def test_components_reachable_transitively(fixture_book: Project) -> None:
    model = model_for(fixture_book)
    # kind order from data/component-kinds.yml: sauces, dips, ..., seasonings
    assert [c.id for c in model.components] == [
        "test-wing-sauce",
        "test-blue-cheese-dip",
        "test-cajun-seasoning",
    ]
    usage = model.usage["test-cajun-seasoning"]
    assert [r.id for r in usage.direct] == []
    assert [r.id for r in usage.indirect] == ["test-citrus-wings"]


def test_draft_component_excluded(fixture_book: Project) -> None:
    assert "test-draft-side" not in {c.id for c in model_for(fixture_book).components}


def test_always_include_pulls_in_dependencies(fixture_book: Project) -> None:
    wings = fixture_book.content_root / "recipes/afc/east/dolphins/test-citrus-wings.md"
    wings.write_text(
        wings.read_text().replace(" {{component:test-wing-sauce}}", ""), encoding="utf-8"
    )
    sauce = fixture_book.content_root / "components/sauces/test-wing-sauce.md"
    sauce.write_text(
        sauce.read_text().replace(
            "status: published\n", "status: published\nalways_include: true\n"
        ),
        encoding="utf-8",
    )
    ids = {c.id for c in model_for(fixture_book).components}
    assert {"test-wing-sauce", "test-cajun-seasoning"} <= ids


def test_unreachable_component_is_omitted(fixture_book: Project) -> None:
    wings = fixture_book.content_root / "recipes/afc/east/dolphins/test-citrus-wings.md"
    wings.write_text(
        wings.read_text().replace(" {{component:test-wing-sauce}}", ""), encoding="utf-8"
    )
    ids = {c.id for c in model_for(fixture_book).components}
    assert ids == {"test-blue-cheese-dip"}


def test_quick_options_use_override_then_quick_buy(fixture_book: Project) -> None:
    model = model_for(fixture_book)
    sliders = model.quick_options["test-buffalo-sliders"]
    assert [(o.component.id, o.text) for o in sliders] == [
        ("test-blue-cheese-dip", "Any chunky store-bought blue cheese dressing")
    ]
    wings = model.quick_options["test-citrus-wings"]
    assert [(o.component.id, o.text) for o in wings] == [("test-wing-sauce", "Bottled wing sauce")]


def test_indexes_group_published_recipes(fixture_book: Project) -> None:
    model = model_for(fixture_book)
    course = next(i for i in model.indexes if i.definition.id == "course")
    by_bucket = {s.bucket.id: [r.id for r in s.recipes] for s in course.sections}
    assert by_bucket["appetizers"] == ["test-buffalo-sliders"]
    assert by_bucket["meals"] == ["test-citrus-wings"]
    assert all("test-draft-nachos" not in ids for ids in by_bucket.values())


def test_menus_and_dishoffs(fixture_book: Project) -> None:
    model = model_for(fixture_book)
    assert [m.id for m in model.menus] == ["test-quick-kickoff"]
    assert [d.id for d in model.dishoffs] == ["test-afc-east-dish-off"]


def test_division_subset_rebuilds_references(fixture_book: Project) -> None:
    root = fixture_book.content_root
    original = root / "recipes/afc/east/dolphins/test-citrus-wings.md"
    other = root / "recipes/nfc/north/packers/test-other-wings.md"
    other.parent.mkdir(parents=True)
    other.write_text(original.read_text().replace("id: test-citrus-wings", "id: test-other-wings"))
    side = root / "components/sides/test-unrelated-side.md"
    side.write_text(
        (root / "components/sides/test-draft-side.md")
        .read_text()
        .replace("test-draft-side", "test-unrelated-side")
        .replace("status: draft", "status: published\nalways_include: true")
    )
    menu = next((root / "menus/game-day").rglob("*.yml"))
    cross = menu.with_name("test-cross-menu.yml")
    cross.write_text(
        menu.read_text()
        .replace("test-quick-kickoff", "test-cross-menu")
        .replace("test-citrus-wings", "test-other-wings")
    )
    dishoff = next((root / "menus/divisions").rglob("*.yml"))
    other_dish = root / "menus/divisions/nfc/north/test-other-dish.yml"
    other_dish.parent.mkdir(parents=True)
    other_dish.write_text(
        dishoff.read_text()
        .replace("test-afc-east-dish-off", "test-other-dish")
        .replace("[test-buffalo-sliders, test-citrus-wings]", "[test-other-wings]")
    )
    loaded = load(fixture_book)
    assert loaded.diagnostics.ok, list(loaded.diagnostics)
    division = loaded.settings.league.division("afc", "east")
    assert division is not None
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links, division=division)
    assert model.division == division
    assert [d.division.key for d in model.divisions] == ["afc-east"]
    selected = {"test-buffalo-sliders", "test-citrus-wings"}
    assert set(model.recipes_by_id) == selected
    assert set(model.quick_options) == selected
    assert set(model.components_by_id) == {
        "test-wing-sauce",
        "test-blue-cheese-dip",
        "test-cajun-seasoning",
    }
    assert {r.id for r in model.usage["test-cajun-seasoning"].indirect} == {"test-citrus-wings"}
    assert all({r.id for r in u.all} <= selected for u in model.usage.values())
    assert all({r.id for r in s.recipes} <= selected for i in model.indexes for s in i.sections)
    assert [m.id for m in model.menus] == ["test-quick-kickoff"]
    assert [d.id for d in model.dishoffs] == ["test-afc-east-dish-off"]
    full = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    assert full.division is None
    assert len(full.divisions) == 8
    assert "test-unrelated-side" in {c.id for c in full.components}
    assert "test-draft-nachos" in full.recipes_by_id
    assert "test-draft-side" in full.components_by_id
    assert "test-other-wings" in {r.id for r in full.recipes}
