"""Cross-document validation over the fixture book."""

from __future__ import annotations

import hashlib
import io
from pathlib import Path

import pytest
from PIL import Image

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
PHOTO_MANIFEST = "data/photo-manifest.yml"


def edit(project: Project, relative: str, old: str, new: str) -> Path:
    path = project.content_root / relative
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {relative}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return path


def errors_for(project: Project, path: Path) -> list[str]:
    return [f"{d.code}: {d.message}" for d in load(project).diagnostics.errors if d.path == path]


def photo_webp(size: tuple[int, int] = (12, 8)) -> bytes:
    image = Image.new("RGB", size, "orange")
    buffer = io.BytesIO()
    image.save(buffer, format="WEBP")
    return buffer.getvalue()


def add_recipe_photo(project: Project, relative: str, name: str, data: bytes) -> tuple[Path, bytes]:
    recipe = edit(
        project,
        relative,
        "status: published",
        f"status: published\nimage: {name}\nphoto_credit: Test photographer",
    )
    (recipe.parent / name).write_bytes(data)
    return recipe, data


def write_photo_manifest(
    project: Project, image_path: Path, data: bytes, *, policy: int = 1, sha256: str | None = None
) -> None:
    relative = image_path.relative_to(project.content_root).as_posix()
    digest = sha256 or hashlib.sha256(data).hexdigest()
    manifest = project.content_root / PHOTO_MANIFEST
    manifest.write_text(
        f'photos:\n  {relative}:\n    sha256: "{digest}"\n    policy: {policy}\n',
        encoding="utf-8",
    )


def test_fixture_book_is_valid(fixture_book: Project) -> None:
    diags = load(fixture_book).diagnostics
    assert diags.errors == []
    assert {(d.code, d.path) for d in diags.warnings} == {
        ("photo", fixture_book.content_root / SLIDERS),
        ("photo", fixture_book.content_root / WINGS),
    }


def test_empty_production_config_is_valid(empty_book: Project) -> None:
    assert load(empty_book).diagnostics.ok


def test_published_recipe_without_image_warns_with_source_path(fixture_book: Project) -> None:
    path = fixture_book.content_root / SLIDERS
    warnings = load(fixture_book).diagnostics.warnings
    assert any(d.path == path and d.code == "photo" and "photo" in d.message for d in warnings)


def test_draft_recipe_without_image_does_not_warn(fixture_book: Project) -> None:
    path = fixture_book.content_root / NACHOS
    assert not any(
        d.path == path and d.code == "photo" for d in load(fixture_book).diagnostics.warnings
    )


def test_published_recipe_with_image_does_not_warn(fixture_book: Project) -> None:
    path = edit(
        fixture_book,
        SLIDERS,
        "status: published",
        "status: published\nimage: test.jpg\nphoto_credit: Test photographer",
    )
    (path.parent / "test.jpg").write_bytes(b"fixture")
    assert not any(
        d.path == path and d.code == "photo" for d in load(fixture_book).diagnostics.warnings
    )


def test_unprepared_published_photo_warns_with_recipe_and_command(fixture_book: Project) -> None:
    path, _ = add_recipe_photo(fixture_book, SLIDERS, "test.webp", photo_webp())

    warnings = [d for d in load(fixture_book).diagnostics.warnings if d.code == "photo-preparation"]

    assert len(warnings) == 1
    assert warnings[0].path == path
    assert "nfl-book prepare-photos" in warnings[0].message
    assert "manifest" in warnings[0].message


def test_valid_manifest_prepared_webp_has_no_preparation_warning(fixture_book: Project) -> None:
    path, data = add_recipe_photo(fixture_book, SLIDERS, "test.webp", photo_webp())
    write_photo_manifest(fixture_book, path.parent / "test.webp", data)

    assert not any(
        d.path == path and d.code == "photo-preparation"
        for d in load(fixture_book).diagnostics.warnings
    )


@pytest.mark.parametrize(
    ("manifest_policy", "manifest_hash", "message"),
    [
        (1, "0" * 64, "hash is stale"),
        (2, None, "policy version is stale"),
    ],
)
def test_stale_photo_manifest_warns(
    fixture_book: Project,
    manifest_policy: int,
    manifest_hash: str | None,
    message: str,
) -> None:
    path, data = add_recipe_photo(fixture_book, SLIDERS, "test.webp", photo_webp())
    write_photo_manifest(
        fixture_book,
        path.parent / "test.webp",
        data,
        policy=manifest_policy,
        sha256=manifest_hash,
    )

    warnings = [d for d in load(fixture_book).diagnostics.warnings if d.code == "photo-preparation"]

    assert len(warnings) == 1
    assert warnings[0].path == path
    assert message in warnings[0].message
    assert "nfl-book prepare-photos" in warnings[0].message


def test_webp_extension_with_non_webp_bytes_warns(fixture_book: Project) -> None:
    path, data = add_recipe_photo(fixture_book, SLIDERS, "test.webp", b"not webp")
    write_photo_manifest(fixture_book, path.parent / "test.webp", data)

    warnings = [d for d in load(fixture_book).diagnostics.warnings if d.code == "photo-preparation"]

    assert len(warnings) == 1
    assert warnings[0].path == path
    assert "not a readable WebP" in warnings[0].message


def test_oversized_photo_warns(fixture_book: Project) -> None:
    data = photo_webp() + b"x" * (1024 * 1024)
    path, _ = add_recipe_photo(fixture_book, SLIDERS, "test.webp", data)
    write_photo_manifest(fixture_book, path.parent / "test.webp", data)

    warnings = [d for d in load(fixture_book).diagnostics.warnings if d.code == "photo-preparation"]

    assert len(warnings) == 1
    assert warnings[0].path == path
    assert "exceeds 1024 KB" in warnings[0].message


def test_webp_exceeding_policy_edge_limit_warns_even_with_matching_manifest(
    fixture_book: Project,
) -> None:
    data = photo_webp((2049, 1000))
    path, _ = add_recipe_photo(fixture_book, SLIDERS, "test.webp", data)
    write_photo_manifest(fixture_book, path.parent / "test.webp", data)

    warnings = [d for d in load(fixture_book).diagnostics.warnings if d.code == "photo-preparation"]

    assert len(warnings) == 1
    assert warnings[0].path == path
    assert "exceeds the 2048 px edge limit" in warnings[0].message


def test_missing_recipe_photo_is_not_a_preparation_warning(fixture_book: Project) -> None:
    path = edit(
        fixture_book,
        SLIDERS,
        "status: published",
        "status: published\nimage: missing.webp\nphoto_credit: Test photographer",
    )

    diags = load(fixture_book).diagnostics

    assert any(d.code == "asset" and d.path == path for d in diags.errors)
    assert not any(d.code == "photo-preparation" and d.path == path for d in diags.warnings)


def test_draft_photo_gets_preparation_warning(fixture_book: Project) -> None:
    path = edit(
        fixture_book,
        NACHOS,
        "status: draft",
        "status: draft\nimage: draft.webp\nphoto_credit: Test photographer",
    )
    (path.parent / "draft.webp").write_bytes(b"not webp")

    warnings = [
        d
        for d in load(fixture_book).diagnostics.warnings
        if d.path == path and d.code == "photo-preparation"
    ]

    assert len(warnings) == 1
    assert "not a readable WebP" in warnings[0].message


def test_malformed_photo_manifest_is_a_diagnostic(fixture_book: Project) -> None:
    path, _ = add_recipe_photo(fixture_book, SLIDERS, "test.webp", photo_webp())
    manifest = fixture_book.content_root / PHOTO_MANIFEST
    manifest.write_text("photos: [not a mapping", encoding="utf-8")

    diags = load(fixture_book).diagnostics

    assert any(d.code == "photo-manifest" and d.path == manifest for d in diags.errors)
    warning = next(d for d in diags.warnings if d.code == "photo-preparation" and d.path == path)
    assert "repair data/photo-manifest.yml before running" in warning.message
    assert "nfl-book prepare-photos" not in warning.message


def test_validator_rejects_manifest_hash_case_the_preparer_rejects(
    fixture_book: Project,
) -> None:
    path, data = add_recipe_photo(fixture_book, SLIDERS, "test.webp", photo_webp())
    manifest = fixture_book.content_root / PHOTO_MANIFEST
    relative = (path.parent / "test.webp").relative_to(fixture_book.content_root).as_posix()
    digest = hashlib.sha256(data).hexdigest().upper()
    manifest.write_text(
        f'photos:\n  {relative}:\n    sha256: "{digest}"\n    policy: 1\n',
        encoding="utf-8",
    )

    diags = load(fixture_book).diagnostics
    warning = next(d for d in diags.warnings if d.code == "photo-preparation" and d.path == path)

    assert any(d.code == "photo-manifest" and d.path == manifest for d in diags.errors)
    assert "repair data/photo-manifest.yml before running" in warning.message
    assert "nfl-book prepare-photos" not in warning.message


def test_unsupported_photo_source_does_not_suggest_unusable_command(
    fixture_book: Project,
) -> None:
    path, _ = add_recipe_photo(fixture_book, SLIDERS, "test.gif", photo_webp())

    warning = next(
        d
        for d in load(fixture_book).diagnostics.warnings
        if d.code == "photo-preparation" and d.path == path
    )

    assert "unsupported source format .gif" in warning.message
    assert ".jpg, .jpeg, .png, or .webp" in warning.message
    assert "nfl-book prepare-photos" not in warning.message


def test_photo_outside_content_root_does_not_suggest_unusable_command(
    fixture_book: Project,
) -> None:
    path = edit(
        fixture_book,
        SLIDERS,
        "status: published",
        "status: published\nimage: ../../../../../outside.jpg\nphoto_credit: Test photographer",
    )
    (fixture_book.content_root.parent / "outside.jpg").write_bytes(b"present")

    warning = next(
        d
        for d in load(fixture_book).diagnostics.warnings
        if d.code == "photo-preparation" and d.path == path
    )

    assert "outside the content root" in warning.message
    assert "update the recipe image path" in warning.message
    assert "nfl-book prepare-photos" not in warning.message


def test_published_recipe_with_missing_image_is_an_error(fixture_book: Project) -> None:
    path = edit(
        fixture_book,
        SLIDERS,
        "status: published",
        "status: published\nimage: missing.jpg\nphoto_credit: Test photographer",
    )
    assert any("image not found: missing.jpg" in e for e in errors_for(fixture_book, path))


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


def ingredient_warnings(project: Project, path: Path) -> list[str]:
    warnings = load(project).diagnostics.warnings
    return [d.message for d in warnings if d.code == "ingredients" and d.path == path]


def test_lone_ingredient_group_holding_every_item_warns(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "\n### To serve\n", "")
    messages = ingredient_warnings(fixture_book, path)
    assert len(messages) == 1
    assert "'Sliders'" in messages[0]


def test_ungrouped_items_before_a_lone_group_do_not_warn(fixture_book: Project) -> None:
    path = edit(fixture_book, SLIDERS, "### Sliders\n", "")
    assert ingredient_warnings(fixture_book, path) == []


def duplicate_warnings(project: Project) -> dict[str, str]:
    warnings = load(project).diagnostics.warnings
    return {d.path.stem: d.message for d in warnings if d.code == "duplicate" and d.path}


def test_published_recipes_with_the_same_title_warn(fixture_book: Project) -> None:
    edit(fixture_book, WINGS, "title: Test Citrus Wings", "title: Test buffalo-sliders!")
    found = duplicate_warnings(fixture_book)
    assert set(found) == {"test-buffalo-sliders", "test-citrus-wings"}
    assert "test-citrus-wings.md" in found["test-buffalo-sliders"]
    assert "title" in found["test-buffalo-sliders"]


def test_published_recipes_with_the_same_source_warn(fixture_book: Project) -> None:
    edit(
        fixture_book,
        WINGS,
        "https://example.com/recipes/test-citrus-wings",
        "https://example.com/recipes/test-buffalo-sliders?ref=fixture&x=1",
    )
    found = duplicate_warnings(fixture_book)
    assert set(found) == {"test-buffalo-sliders", "test-citrus-wings"}
    assert "source" in found["test-citrus-wings"]


def test_draft_duplicate_does_not_warn(fixture_book: Project) -> None:
    edit(fixture_book, NACHOS, "title: Test Draft Nachos", "title: Test Buffalo Sliders")
    assert duplicate_warnings(fixture_book) == {}


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


def test_timeline_rejects_unknown_time(fixture_book: Project) -> None:
    path = edit(fixture_book, MENU, "at: -1h30m", "at: -90m")
    errors = errors_for(fixture_book, path)
    assert any(e.startswith("schema: timeline.1.at:") and "-1h30m" in e for e in errors)


def test_timeline_steps_must_be_in_time_order(fixture_book: Project) -> None:
    path = edit(fixture_book, MENU, "at: -30m", "at: -4h")
    assert errors_for(fixture_book, path) == [
        "schema: timeline: steps must be in time order: "
        "step 2 (-4h) is earlier than step 1 (-1h30m) but listed after it"
    ]


def test_timeline_recipe_must_be_on_the_menu(fixture_book: Project) -> None:
    path = edit(
        fixture_book,
        MENU,
        "recipe: test-citrus-wings\n    task: Marinate",
        "recipe: test-draft-nachos\n    task: Marinate",
    )
    assert errors_for(fixture_book, path) == [
        "reference: timeline.1.recipe: 'test-draft-nachos' is not one of this menu's recipes"
    ]


def test_timeline_task_must_not_be_empty(fixture_book: Project) -> None:
    path = edit(fixture_book, MENU, "task: Heat the oven.", "task: '  '")
    assert any(e.startswith("schema: timeline.2.task:") for e in errors_for(fixture_book, path))


def test_timeline_task_is_short(fixture_book: Project) -> None:
    path = edit(fixture_book, MENU, "task: Heat the oven.", "task: " + "x" * 81)
    assert any(e.startswith("schema: timeline.2.task:") for e in errors_for(fixture_book, path))


def test_timeline_has_at_most_six_steps(fixture_book: Project) -> None:
    extra = "  - at: halftime\n    task: Refill the chips.\n"
    path = fixture_book.content_root / MENU
    path.write_text(path.read_text(encoding="utf-8") + extra * 2, encoding="utf-8")
    assert any(
        e.startswith("schema: timeline:") and "6" in e for e in errors_for(fixture_book, path)
    )


def test_timeline_may_not_be_empty(fixture_book: Project) -> None:
    path = fixture_book.content_root / MENU
    text = path.read_text(encoding="utf-8")
    path.write_text(text[: text.index("timeline:")] + "timeline: []\n", encoding="utf-8")
    assert any(e.startswith("schema: timeline:") for e in errors_for(fixture_book, path))


def test_dishoff_timeline_recipe_must_be_on_the_dishoff(fixture_book: Project) -> None:
    path = edit(fixture_book, DISHOFF, "recipe: test-citrus-wings", "recipe: test-ghost")
    assert errors_for(fixture_book, path) == [
        "reference: timeline.0.recipe: 'test-ghost' is not one of this menu's recipes"
    ]


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
    assert {d.code for d in diags.warnings} == {"photo", "shortlink"}


def test_validate_raises_and_filters_by_path(fixture_book: Project) -> None:
    edit(fixture_book, SLIDERS, "course: appetizers", "course: brunch")
    with pytest.raises(ValidationFailed) as excinfo:
        validate(fixture_book)
    assert all(
        d.path and d.path.name == "test-buffalo-sliders.md"
        for d in excinfo.value.diagnostics.errors
    )
    assert validate(fixture_book, [fixture_book.content_root / WINGS]).ok
