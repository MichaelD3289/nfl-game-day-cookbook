"""The shared recipe catalog (``recipes.json``) behind Browse recipes and later site tools."""

from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from PIL import Image

from nfl_book import pipeline
from nfl_book.catalog import CATALOG_FILE, LEAGUE_FACETS, recipe_catalog, write_catalog
from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.project import Project
from nfl_book.website import build_website


def _catalog(project: Project) -> dict[str, Any]:
    site = build_website(project, render=False).document.parent
    data: dict[str, Any] = json.loads((site / CATALOG_FILE).read_text(encoding="utf-8"))
    return data


def _entry(catalog: dict[str, Any], recipe_id: str) -> dict[str, Any]:
    entry: dict[str, Any] = next(r for r in catalog["recipes"] if r["id"] == recipe_id)
    return entry


def _add_photo(project: Project) -> None:
    recipe = next(project.recipes_dir.rglob("test-citrus-wings.md"))
    recipe.write_text(
        recipe.read_text().replace(
            "status: published",
            "status: published\nimage: test-wings.jpg\nphoto_credit: Synthetic fixture",
        )
    )
    buffer = io.BytesIO()
    Image.new("RGB", (400, 400), "orange").save(buffer, format="JPEG")
    (recipe.parent / "test-wings.jpg").write_bytes(buffer.getvalue())


def test_catalog_lists_published_recipes_in_book_order(fixture_book: Project) -> None:
    catalog = _catalog(fixture_book)
    assert catalog["version"] == 1
    assert catalog["edition"]
    assert [r["id"] for r in catalog["recipes"]] == ["test-buffalo-sliders", "test-citrus-wings"]
    text = json.dumps(catalog)
    assert "test-draft-nachos" not in text
    assert "test-draft-side" not in text
    assert "last_reviewed" not in text


def test_catalog_entry_fields(fixture_book: Project) -> None:
    catalog = _catalog(fixture_book)
    sliders = _entry(catalog, "test-buffalo-sliders")
    assert sliders["title"] == "Test Buffalo Sliders"
    assert sliders["url"] == "recipe-test-buffalo-sliders.html"
    assert sliders["photo"] is None
    assert sliders["course"] == "appetizers"
    assert sliders["course_label"] == "Appetizer"
    assert sliders["team"] == {
        "slug": "bills",
        "name": "Buffalo Bills",
        "short_name": "Bills",
        "abbreviation": "BUF",
    }
    assert sliders["conference"] == "afc"
    assert sliders["division"] == "afc-east"
    assert sliders["division_name"] == "AFC East"
    assert sliders["servings"] == [4, 6]
    assert sliders["yield"] == "12 sliders"
    assert sliders["prep"] == "15 min"
    assert sliders["cook"] == "20 min"
    assert sliders["components"] == ["test-blue-cheese-dip"]
    assert sliders["facets"] == {
        "course": ["appetizers"],
        "main-ingredient": ["poultry"],
        "practical-time": ["31-to-60-minutes"],
        "ingredient-cost": ["moderate"],
        "conference": ["afc"],
        "division": ["afc-east"],
        "team": ["bills"],
    }
    wings = _entry(catalog, "test-citrus-wings")
    assert wings["prep"] is None and wings["cook"] is None
    # Nested components follow the component that uses them.
    assert wings["components"] == ["test-wing-sauce", "test-cajun-seasoning"]
    assert wings["facets"]["team"] == ["dolphins"]


def test_facets_follow_indexes_then_league(fixture_book: Project) -> None:
    catalog = _catalog(fixture_book)
    facets = catalog["facets"]
    indexes = yaml.safe_load((fixture_book.data_dir / "indexes.yml").read_text())["indexes"]
    assert [f["id"] for f in facets] == [i["id"] for i in indexes] + list(LEAGUE_FACETS)
    course = facets[0]
    assert course["title"] == "Course"
    assert course["source"] == "index"
    assert [o["id"] for o in course["options"]] == [b["id"] for b in indexes[0]["buckets"]]
    league = {f["id"]: f for f in facets if f["source"] == "league"}
    assert league["conference"]["options"] == [{"id": "afc", "label": "AFC"}]
    assert league["division"]["options"] == [{"id": "afc-east", "label": "AFC East"}]
    # Only teams with a published recipe; the draft-only Jets are left out.
    assert league["team"]["options"] == [
        {"id": "bills", "label": "Buffalo Bills", "group": "AFC East"},
        {"id": "dolphins", "label": "Miami Dolphins", "group": "AFC East"},
    ]


def test_new_index_becomes_a_facet_without_code_changes(fixture_book: Project) -> None:
    path = fixture_book.data_dir / "indexes.yml"
    data = yaml.safe_load(path.read_text())
    data["indexes"].append(
        {
            "id": "test-heat",
            "title": "Index by Test Heat",
            "kind": "field",
            "field": "index.test_heat",
            "required": False,
            "buckets": [{"id": "mild", "label": "Mild"}, {"id": "hot", "label": "Hot"}],
        }
    )
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    recipe = next(fixture_book.recipes_dir.rglob("test-citrus-wings.md"))
    recipe.write_text(recipe.read_text().replace("  cost:", "  test_heat: hot\n  cost:"))
    catalog = _catalog(fixture_book)
    heat = next(f for f in catalog["facets"] if f["id"] == "test-heat")
    assert heat["title"] == "Test Heat"
    assert [o["id"] for o in heat["options"]] == ["mild", "hot"]
    assert _entry(catalog, "test-citrus-wings")["facets"]["test-heat"] == ["hot"]
    assert _entry(catalog, "test-buffalo-sliders")["facets"]["test-heat"] == []
    browse = (fixture_book.generated_dir / "site/browse.qmd").read_text()
    assert 'data-facet="test-heat"' in browse


def test_catalog_targets_exist_and_ship_with_the_site(fixture_book: Project) -> None:
    _add_photo(fixture_book)
    catalog = _catalog(fixture_book)
    site = fixture_book.generated_dir / "site"
    wings = _entry(catalog, "test-citrus-wings")
    assert wings["photo"] and wings["photo"].startswith("assets/")
    assert wings["photo_size"] > 0
    for recipe in catalog["recipes"]:
        assert (site / recipe["url"].replace(".html", ".qmd")).is_file(), recipe["url"]
        if recipe["photo"]:
            assert (site / recipe["photo"]).is_file(), recipe["photo"]
    config = yaml.safe_load((site / "_quarto.yml").read_text())
    assert "recipes.json" in config["project"]["resources"]
    assert "browse.js" in config["project"]["resources"]
    assert (site / "browse.js").read_text().startswith("// Browse recipes")


def test_reserved_facet_ids_fail_validation(fixture_book: Project) -> None:
    path = fixture_book.data_dir / "indexes.yml"
    data = yaml.safe_load(path.read_text())
    data["indexes"].append(
        {
            "id": "team",
            "title": "Index by Team",
            "kind": "field",
            "field": "index.team_pick",
            "buckets": [{"id": "x", "label": "X"}],
        }
    )
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    with pytest.raises(ValidationFailed) as failed:
        pipeline.validate(fixture_book)
    errors = failed.value.diagnostics.errors
    assert [(d.code, d.path) for d in errors] == [("config", path)]
    assert "'team' is reserved" in errors[0].message


def test_catalog_can_be_built_and_written_directly(fixture_book: Project, tmp_path: Path) -> None:
    from nfl_book.digital import prepare_pages

    pages, _, _, model = prepare_pages(fixture_book, tmp_path / "build", web=True)
    diags = Diagnostics()
    catalog = recipe_catalog(model, pages, diags, edition="9.9.9")
    assert diags.ok
    assert catalog["edition"] == "9.9.9"
    target = tmp_path / "recipes.json"
    write_catalog(catalog, target)
    text = target.read_text(encoding="utf-8")
    assert text.endswith("}\n")
    assert json.loads(text) == catalog
