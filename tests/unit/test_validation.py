"""Cross-document validation over the fixture book."""

from __future__ import annotations

from pathlib import Path

import pytest

from nfl_book.errors import ValidationFailed
from nfl_book.pipeline import load, validate
from nfl_book.project import Project

SLIDERS = "recipes/afc/east/bills/test-buffalo-sliders.md"
WINGS = "recipes/afc/east/dolphins/test-citrus-wings.md"
NACHOS = "recipes/afc/east/jets/test-draft-nachos.md"
SAUCE = "components/sauces/test-wing-sauce.md"
SEASONING = "components/seasonings/test-cajun-seasoning.md"
DIP = "components/dips/test-blue-cheese-dip.md"
MENU = "menus/game-day/fast-day/test-quick-kickoff.yml"
DISHOFF = "menus/divisions/afc/east/test-afc-east-dish-off.yml"


def edit(project: Project, relative: str, old: str, new: str) -> Path:
    path = project.content_root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {relative}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return path


def errors_for(project: Project, path: Path) -> list[str]:
    return [f"{d.code}: {d.message}" for d in load(project).diagnostics.errors if d.path == path]


def test_fixture_book_is_valid(fixture_book: Project) -> None:
    diags = load(fixture_book).diagnostics
    assert diags.errors == []
    assert diags.warnings == []


def test_empty_production_config_is_valid(empty_book: Project) -> None:
    assert load(empty_book).diagnostics.ok


def test_published_recipe_requires_index_values(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "  cost: moderate\n", "")
    assert any(e.startswith("index:") and "cost" in e for e in errors_for(fixture_book, path))


def test_draft_recipe_may_omit_index_values(fixture_book: Project) -> None:
    path = fixture_book.content_root / NACHOS
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("  cost: pantry-friendly\n", ""), encoding="utf-8")
    assert errors_for(fixture_book, path) == []


def test_unknown_bucket(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "cost: moderate", "cost: priceless")
    assert any("priceless" in e for e in errors_for(fixture_book, path))


def test_unknown_course(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "course: appetizers", "course: brunch")
    assert any("brunch" in e for e in errors_for(fixture_book, path))


def test_unknown_index_key(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "  cost: moderate\n", "  cost: moderate\n  spice: hot\n")
    assert any("index.spice: unknown index key" in e for e in errors_for(fixture_book, path))


def test_single_value_index_rejects_list(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "cost: moderate", "cost: [moderate, premium]")
    assert any("single value" in e for e in errors_for(fixture_book, path))


def test_unknown_component_reference(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "test-blue-cheese-dip}}", "test-ranch}}")
    errors = errors_for(fixture_book, path)
    assert "reference: unknown component 'test-ranch'" in errors


def test_published_recipe_cannot_use_draft_component(fixture_book: Project) -> None:
    edit(fixture_book, DIP, "status: published", "status: draft")
    errors = errors_for(fixture_book, fixture_book.content_root / SLIDERS)
    assert any("whose status is draft" in e for e in errors)


def test_draft_recipe_may_use_draft_component(fixture_book: Project) -> None:
    assert errors_for(fixture_book, fixture_book.content_root / NACHOS) == []


def test_quick_option_override_must_match_a_reference(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "  test-blue-cheese-dip: Any", "  test-wing-sauce: Any")
    assert any("quick_options.test-wing-sauce" in e for e in errors_for(fixture_book, path))


def test_cycle_is_rejected(fixture_book: Project) -> None:
    edit(fixture_book, SEASONING, "- 1 tsp cayenne", "- 1 tsp sauce {{component:test-wing-sauce}}")
    cycles = [d for d in load(fixture_book).diagnostics.errors if d.code == "cycle"]
    assert len(cycles) == 1
    assert "test-wing-sauce" in cycles[0].message
    assert "test-cajun-seasoning" in cycles[0].message
    assert cycles[0].path is not None and cycles[0].path.suffix == ".md"


def test_unused_published_component_warns(fixture_book: Project) -> None:
    edit(fixture_book, WINGS, " {{component:test-wing-sauce}}", "")
    warnings = load(fixture_book).diagnostics.warnings
    unused = {d.path.stem for d in warnings if d.code == "unused" and d.path}
    assert unused == {"test-wing-sauce", "test-cajun-seasoning"}


def test_always_include_silences_unused_warning(fixture_book: Project) -> None:
    edit(fixture_book, WINGS, " {{component:test-wing-sauce}}", "")
    edit(fixture_book, SAUCE, "status: published\n", "status: published\nalways_include: true\n")
    warnings = load(fixture_book).diagnostics.warnings
    assert not [d for d in warnings if d.code == "unused"]


def test_menu_unknown_recipe(fixture_book: Project) -> None:
    path = edit(fixture_book, MENU, "test-citrus-wings]", "test-ghost]")
    assert "reference: unknown recipe 'test-ghost'" in errors_for(fixture_book, path)


def test_published_menu_cannot_list_draft_recipe(fixture_book: Project) -> None:
    path = edit(fixture_book, MENU, "test-citrus-wings]", "test-draft-nachos]")
    assert any("is draft" in e for e in errors_for(fixture_book, path))


def test_dishoff_recipe_must_be_in_division(fixture_book: Project, write: object) -> None:
    other = fixture_book.content_root / "recipes/afc/north/steelers/test-draft-nachos.md"
    other.parent.mkdir(parents=True)
    (fixture_book.content_root / NACHOS).rename(other)
    edit(
        fixture_book,
        other.relative_to(fixture_book.content_root).as_posix(),
        "status: draft",
        "status: published",
    )
    path = edit(fixture_book, DISHOFF, "test-citrus-wings]", "test-draft-nachos]")
    assert any("belongs to AFC North" in e for e in errors_for(fixture_book, path))


def test_missing_shortlink_is_a_clear_error(fixture_book: Project) -> None:
    fixture_book.shortlinks_file.unlink()
    errors = [d for d in load(fixture_book).diagnostics.errors if d.code == "shortlink"]
    assert {d.path.name for d in errors if d.path} == {
        "test-buffalo-sliders.md",
        "test-citrus-wings.md",
        "test-blue-cheese-dip.md",
    }
    assert all("prepare-links" in d.message for d in errors)


def test_missing_shortlink_is_only_a_warning_when_not_required(fixture_book: Project) -> None:
    fixture_book.shortlinks_file.unlink()
    diags = load(fixture_book, require_shortlinks=False).diagnostics
    assert diags.ok
    assert {d.code for d in diags.warnings} == {"shortlink"}


def test_validate_raises_and_filters_by_path(fixture_book: Project) -> None:
    edit(fixture_book, SLIDERS, "course: appetizers", "course: brunch")
    with pytest.raises(ValidationFailed) as excinfo:
        validate(fixture_book)
    assert all(
        d.path and d.path.name == "test-buffalo-sliders.md" for d in excinfo.value.diagnostics
    )
    assert validate(fixture_book, [fixture_book.content_root / WINGS]).ok
