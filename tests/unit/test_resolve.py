"""Publication rules: what reaches the book, and in what order."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from nfl_book.errors import Diagnostics
from nfl_book.models.common import Status
from nfl_book.pipeline import build_media, load
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
    # The copy keeps no timeline: its steps name AFC East recipes it no longer has.
    other_dish.write_text(
        dishoff.read_text()
        .split("timeline:")[0]
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
    assert set(model.components_by_id) == {c.id for c in model.components}
    assert {r.id for r in model.usage["test-cajun-seasoning"].indirect} == {"test-citrus-wings"}
    assert all({r.id for r in u.all} <= selected for u in model.usage.values())
    assert all({r.id for r in s.recipes} <= selected for i in model.indexes for s in i.sections)
    assert [m.id for m in model.menus] == ["test-quick-kickoff"]
    assert [d.id for d in model.dishoffs] == ["test-afc-east-dish-off"]
    full = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    assert full.division is None
    assert len(full.divisions) == 8
    assert "test-unrelated-side" in {c.id for c in full.components}
    assert "test-draft-nachos" not in full.recipes_by_id
    assert "test-draft-side" not in full.components_by_id
    assert "test-other-wings" in {r.id for r in full.recipes}


EXCLUDED_RECIPES = {"test-draft-nachos", "test-retired-nachos"}
EXCLUDED_COMPONENTS = {"test-draft-side", "test-retired-side"}


def test_published_model_holds_no_draft_or_retired_item(fixture_book: Project) -> None:
    model = model_for(fixture_book)
    assert not EXCLUDED_RECIPES & {r.id for r in model.recipes}
    assert not EXCLUDED_RECIPES & set(model.recipes_by_id)
    assert not EXCLUDED_COMPONENTS & {c.id for c in model.components}
    assert not EXCLUDED_COMPONENTS & set(model.components_by_id)
    assert not EXCLUDED_COMPONENTS & set(model.usage)
    for recipe in model.recipes:
        assert not EXCLUDED_COMPONENTS & {c.id for c in model.components_for(recipe)}
    for recipe in (r for r in load(fixture_book).content.recipes if r.id in EXCLUDED_RECIPES):
        assert model.components_for(recipe) == ()


def test_components_for_lists_nested_components_once_in_order(fixture_book: Project) -> None:
    model = model_for(fixture_book)
    wings = model.recipes_by_id["test-citrus-wings"]
    assert [c.id for c in model.components_for(wings)] == [
        "test-wing-sauce",
        "test-cajun-seasoning",
    ]


def test_preview_include_admits_drafts_but_not_retired(fixture_book: Project) -> None:
    loaded = load(fixture_book)
    model = resolve(
        loaded.settings,
        loaded.content,
        loaded.shortlinks.links,
        include=lambda status: status is not Status.RETIRED,
    )
    assert "test-draft-nachos" in {r.id for r in model.recipes}
    assert "test-draft-nachos" in model.recipes_by_id
    assert "test-draft-side" in {c.id for c in model.components}
    assert "test-draft-side" in model.components_by_id
    assert "test-draft-side" in model.usage
    nachos = model.recipes_by_id["test-draft-nachos"]
    assert [c.id for c in model.components_for(nachos)] == ["test-draft-side"]
    assert not EXCLUDED_RECIPES - {"test-draft-nachos"} & set(model.recipes_by_id)
    assert "test-retired-side" not in model.components_by_id
    assert "test-retired-side" not in model.usage


def test_division_model_holds_only_components_its_recipes_reach(fixture_book: Project) -> None:
    loaded = load(fixture_book)
    division = loaded.settings.league.division("afc", "east")
    assert division is not None
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links, division=division)
    reached = {c.id for r in model.recipes for c in model.components_for(r)}
    assert set(model.components_by_id) == reached == {c.id for c in model.components}
    assert not EXCLUDED_COMPONENTS & reached


def _add_media_sources(root: Path, rel: str, *, image: bool) -> None:
    """Give an item a source URL and, for a recipe, a small real photo."""
    path = root / rel
    extra = f"source:\n  url: https://example.com/{path.stem}\n"
    if image:
        Image.new("RGB", (40, 30), "red").save(path.parent / f"{path.stem}.jpg")
        extra += f"image: {path.stem}.jpg\nphoto_credit: Test\n"
    path.write_text(path.read_text().replace("\n---\n", "\n" + extra + "---\n", 1))


def test_build_media_skips_drafts_and_retired_items(fixture_book: Project, tmp_path: Path) -> None:
    root = fixture_book.content_root
    excluded = {
        "recipes/afc/east/jets/test-draft-nachos.md": True,
        "recipes/afc/east/jets/test-retired-nachos.md": True,
        "components/sides/test-draft-side.md": False,
        "components/sides/test-retired-side.md": False,
    }
    for rel, image in excluded.items():
        _add_media_sources(root, rel, image=image)
    # The same setup on published items proves the test can see media when there is any.
    _add_media_sources(root, "recipes/afc/east/bills/test-buffalo-sliders.md", image=True)
    _add_media_sources(root, "components/sauces/test-wing-sauce.md", image=False)

    loaded = load(fixture_book)
    model = resolve(loaded.settings, loaded.content, loaded.shortlinks.links)
    diags = Diagnostics()
    media, _ = build_media(
        fixture_book, model, tmp_path / "build", diags, loaded.settings.book.photos.print
    )
    assert diags.ok, list(diags)
    assert "recipe:test-buffalo-sliders" in media.qr
    assert "component:test-wing-sauce" in media.qr
    assert "recipe:test-buffalo-sliders" in media.images
    keys = set(media.qr) | set(media.images)
    assert not any(i in key for key in keys for i in EXCLUDED_RECIPES | EXCLUDED_COMPONENTS)
    assert not any(
        i in p.name
        for p in fixture_book.qr_dir.glob("*.png")
        for i in EXCLUDED_RECIPES | EXCLUDED_COMPONENTS
    )
