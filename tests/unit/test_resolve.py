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
