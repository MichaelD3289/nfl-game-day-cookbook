import json
from pathlib import Path

from nfl_book.errors import Diagnostics
from nfl_book.website_check import check_site


def test_local_links_and_fragments_are_checked(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text(
        '<a href="recipe.html#instructions">Recipe</a>'
        '<a href="https://example.com">Source</a><img src="assets/photo.png">'
    )
    (tmp_path / "recipe.html").write_text('<h2 id="instructions">Method</h2>')
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets/photo.png").write_bytes(b"photo")
    diags = Diagnostics()
    check_site(tmp_path, diags)
    assert not diags.errors
    (tmp_path / "recipe.html").write_text("<h2>Missing anchor</h2>")
    (tmp_path / "assets/photo.png").unlink()
    diags = Diagnostics()
    check_site(tmp_path, diags)
    assert len(diags.errors) == 2
    assert all(d.path == tmp_path / "index.html" for d in diags.errors)


def test_print_pages_are_checked_like_links(tmp_path: Path) -> None:
    (tmp_path / "recipe.html").write_text(
        '<div class="print-bar" data-print-pages="component-a.html component-b.html"></div>'
    )
    (tmp_path / "component-a.html").write_text("<h1>A</h1>")
    diags = Diagnostics()
    check_site(tmp_path, diags)
    assert [d.message for d in diags.errors] == ["Missing local target: component-b.html"]
    assert diags.errors[0].path == tmp_path / "recipe.html"


def test_print_components_are_checked_like_links(tmp_path: Path) -> None:
    (tmp_path / "menu.html").write_text(
        '<div class="print-bar print-menu" data-print-pages="recipe-a.html"'
        ' data-print-components="component-a.html component-b.html"></div>'
    )
    (tmp_path / "recipe-a.html").write_text("<h1>Recipe</h1>")
    (tmp_path / "component-a.html").write_text("<h1>A</h1>")
    diags = Diagnostics()
    check_site(tmp_path, diags)
    assert [d.message for d in diags.errors] == ["Missing local target: component-b.html"]
    assert diags.errors[0].path == tmp_path / "menu.html"


def test_recipe_catalog_targets_are_checked(tmp_path: Path) -> None:
    (tmp_path / "recipe-a.html").write_text("<h1>A</h1>")
    (tmp_path / "assets").mkdir()
    (tmp_path / "assets/a.jpg").write_bytes(b"photo")
    catalog = tmp_path / "recipes.json"
    catalog.write_text(
        json.dumps(
            {
                "recipes": [
                    {"url": "recipe-a.html", "photo": "assets/a.jpg"},
                    {"url": "recipe-b.html", "photo": None},
                    {"url": "recipe-a.html", "photo": "assets/missing.jpg"},
                ]
            }
        )
    )
    diags = Diagnostics()
    check_site(tmp_path, diags)
    assert [(d.code, d.message, d.path) for d in diags.errors] == [
        ("website-link", "Missing catalog target: recipe-b.html", catalog),
        ("website-link", "Missing catalog target: assets/missing.jpg", catalog),
    ]


def test_invalid_recipe_catalog_is_reported(tmp_path: Path) -> None:
    catalog = tmp_path / "recipes.json"
    catalog.write_text("{not json")
    diags = Diagnostics()
    check_site(tmp_path, diags)
    assert [(d.code, d.path) for d in diags.errors] == [("website-link", catalog)]
    assert diags.errors[0].message.startswith("Invalid recipe catalog")
