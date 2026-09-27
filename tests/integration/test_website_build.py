"""Render synthetic content with the same Quarto compiler used by releases."""

import json
import shutil
from html.parser import HTMLParser

import pytest

from nfl_book.project import Project
from nfl_book.qr import qr_png
from nfl_book.website import build_website


def _elements(html: str, tag: str, css_class: str) -> list[dict[str, str | None]]:
    """Attributes of each ``tag`` carrying ``css_class``, however Quarto serialized them.

    Quarto re-serializes pages, so a bare ``hidden`` may come out as ``hidden=""``
    and attribute order can change; compare attributes, not markup.
    """
    found: list[dict[str, str | None]] = []

    class Finder(HTMLParser):
        def handle_starttag(self, name: str, attrs: list[tuple[str, str | None]]) -> None:
            data = dict(attrs)
            if name == tag and css_class in (data.get("class") or "").split():
                found.append(data)

    Finder().feed(html)
    return found


def _head(html: str) -> tuple[list[str], list[dict[str, str | None]]]:
    """JSON-LD script bodies and ``<link>`` attributes found inside ``<head>``."""
    scripts: list[str] = []
    links: list[dict[str, str | None]] = []

    class Head(HTMLParser):
        in_head = False
        in_json = False

        def handle_starttag(self, name: str, attrs: list[tuple[str, str | None]]) -> None:
            data = dict(attrs)
            if name == "head":
                self.in_head = True
            elif self.in_head and name == "script" and data.get("type") == "application/ld+json":
                self.in_json = True
                scripts.append("")
            elif self.in_head and name == "link":
                links.append(data)

        def handle_endtag(self, name: str) -> None:
            if name == "head":
                self.in_head = False
            elif name == "script":
                self.in_json = False

        def handle_data(self, data: str) -> None:
            if self.in_json:
                scripts[-1] += data

    Head().feed(html)
    return scripts, links


@pytest.mark.skipif(shutil.which("quarto") is None, reason="Quarto not installed")
def test_rendered_website_has_cards_search_and_no_print_markup(fixture_book: Project) -> None:
    recipe = next(fixture_book.recipes_dir.rglob("test-citrus-wings.md"))
    recipe.write_text(
        recipe.read_text().replace(
            "status: published",
            "status: published\nimage: fixture.png\nphoto_credit: Synthetic fixture",
        )
    )
    photo = qr_png("https://example.com/synthetic-photo")
    (recipe.parent / "fixture.png").write_bytes(photo)
    fixture_book.dist_dir.mkdir(parents=True)
    pdf = fixture_book.dist_dir / "existing-book.pdf"
    pdf.write_bytes(b"unchanged PDF")
    result = build_website(fixture_book)
    assert pdf.read_bytes() == b"unchanged PDF"
    assert result.site is not None
    wings = (result.site / "recipe-test-citrus-wings.html").read_text()
    assert 'class="recipe-header"' in wings
    assert 'quick-card"' in wings
    assert "::: {" not in wings
    assert '<h1 class="title"' not in wings
    assert "component-test-wing-sauce.html#component-test-wing-sauce" in wings
    assert '<span class="qty" data-q="2" data-unit="lb">2 lb</span>' in wings
    scalers = _elements(wings, "div", "scaler")
    assert len(scalers) == 1
    assert scalers[0].get("data-servings") == "4"
    assert "hidden" in scalers[0]  # revealed by scale.js
    assert (result.site / "scale.js").is_file()
    bars = _elements(wings, "div", "print-bar")
    assert len(bars) == 1
    assert "hidden" in bars[0]  # revealed by print.js
    assert (result.site / "print.js").is_file()
    search = json.loads((result.site / "search.json").read_text())
    assert any("Test Citrus Wings" in entry["title"] for entry in search)
    assert not any("test-draft" in entry["href"] for entry in search)

    assert (recipe.parent / "fixture.png").read_bytes() == photo
    assert (result.site / "assets/recipe-test-citrus-wings.webp").is_file()
    assert not (result.site / "assets/recipe-test-citrus-wings.png").exists()
    assert (result.site / "assets/qr-recipe-test-citrus-wings.png").is_file()
    assert (result.site / "assets/qr-component-test-wing-sauce.png").is_file()
    assert "Scan to open on your phone" in wings
    assert "assets/recipe-test-citrus-wings.webp" in wings
    assert 'loading="lazy"' in wings

    scripts, links = _head(wings)
    assert len(scripts) == 1
    data = json.loads(scripts[0])
    assert data["@type"] == "Recipe"
    assert data["name"] == "Test Citrus Wings"
    assert data["image"].endswith("assets/recipe-test-citrus-wings.webp")
    canonical = [link for link in links if link.get("rel") == "canonical"]
    assert len(canonical) == 1
    assert (canonical[0].get("href") or "").endswith("/recipe-test-citrus-wings.html")
    sauce = (result.site / "component-test-wing-sauce.html").read_text()
    assert "application/ld+json" not in sauce

    for page in result.site.glob("*.html"):
        assert "</span> ##" not in page.read_text(), page.name
