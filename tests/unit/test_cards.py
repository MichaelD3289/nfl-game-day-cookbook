"""Recipe cards use only synthetic content and separate output directories."""

import pytest
import yaml

from nfl_book.cards import build_cards
from nfl_book.errors import ValidationFailed
from nfl_book.project import Project


def test_cards_sources_are_separate_and_published(fixture_book: Project) -> None:
    result = build_cards(fixture_book, pdf=False)
    assert result.document.parent == fixture_book.generated_dir / "cards"
    assert "latex-auto-install: false" in result.document.read_text()
    assert not fixture_book.book_build_dir.exists()
    text = "\n".join(p.read_text() for p in result.document.parent.glob("pages/*.qmd"))
    assert "test-draft" not in text
    assert "\\CardStart{" in text
    assert text.index("Ingredients") < text.index("\\CardInstructions")
    assert "\\ComponentRef" not in text
    assert "component-test-" in text
    assert "\\CardSource" in text
    assert "../qr/" in text
    assert "Yield:" in text
    assert "Buffalo Bills — Buffalo" in text
    assert "**Sliders**\n\n- " in text
    assert (
        "paperwidth=4.0in,paperheight=6.0in"
        in (result.document.parent / "styles/card-geometry.tex").read_text()
    )
    stale = result.document.parent / "pages/stale.qmd"
    stale.write_text("stale")
    build_cards(fixture_book, pdf=False)
    assert not stale.exists()


def test_invalid_card_dimensions_name_config(fixture_book: Project) -> None:
    path = fixture_book.data_dir / "book.yml"
    data = yaml.safe_load(path.read_text())
    data["cards"] = {"width_inches": -1}
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValidationFailed) as exc:
        build_cards(fixture_book, pdf=False)
    assert any(d.path == path for d in exc.value.diagnostics.errors)


def test_cards_escape_titles_and_fallback_links(fixture_book: Project) -> None:
    path = fixture_book.data_dir / "book.yml"
    data = yaml.safe_load(path.read_text())
    data.pop("website_url", None)
    data["cards"]["width_inches"] = 5
    data["cards"]["height_inches"] = 7
    path.write_text(yaml.safe_dump(data))
    recipe = next(fixture_book.content_root.glob("recipes/**/test-*.md"))
    text = recipe.read_text()
    # Keep the fixture's schema intact while exercising TeX macro arguments.
    text = text.replace("title: ", "title: Fish & Chips 50% ", 1)
    recipe.write_text(text)
    result = build_cards(fixture_book, pdf=False)
    fragments = "\n".join(p.read_text() for p in result.document.parent.glob("pages/*.qmd"))
    assert r"Fish \& Chips 50\%" in fragments
    assert r"\href{}" not in fragments
    assert "available in the cookbook" in fragments
    assert (
        "paperwidth=5.0in,paperheight=7.0in"
        in (result.document.parent / "styles/card-geometry.tex").read_text()
    )
