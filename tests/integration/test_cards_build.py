"""Rendered cards preserve synthetic long instructions and enforce source-based limits."""

import shutil

import pytest
import yaml
from pypdf import PdfReader

from nfl_book.cards import build_cards
from nfl_book.errors import ValidationFailed
from nfl_book.postbuild import load_pagemap
from nfl_book.project import Project


@pytest.mark.pdf
@pytest.mark.skipif(shutil.which("quarto") is None, reason="Quarto is not installed")
def test_long_cards_continue_and_strict_overflow_names_source(fixture_book: Project) -> None:
    source = fixture_book.content_root / "recipes/afc/east/bills/test-buffalo-sliders.md"
    text = source.read_text().replace("1 lb ground chicken", "⅛ lb ground chicken")
    instructions = "\n".join(
        f"{i}. Stir the synthetic test mixture carefully, scrape the bowl and rest before serving."
        for i in range(1, 41)
    )
    text = text.replace(
        "1. Form 12 patties and cook until done.\n2. Spoon the **dip** over each slider and serve.",
        instructions + "\n41. Serve the final sentinel mango platter.",
    )
    source.write_text(text)
    config = fixture_book.data_dir / "book.yml"
    data = yaml.safe_load(config.read_text())
    data["cards"]["max_pages"] = 2
    config.write_text(yaml.safe_dump(data))
    result = build_cards(fixture_book)
    assert result.pdf is not None
    reader = PdfReader(result.pdf)
    assert all(tuple(float(v) for v in p.mediabox[2:]) == (288, 432) for p in reader.pages)
    contents = "\n".join(p.extract_text() for p in reader.pages)
    assert "final sentinel mango platter" in contents
    assert contents.count("Test Buffalo Sliders") >= 3
    assert "Test Draft" not in contents
    pagemap = load_pagemap(fixture_book.generated_dir / "cards/pagemap.json")
    first = pagemap["recipe:test-buffalo-sliders"]
    last = pagemap["recipe:test-buffalo-sliders:end"]
    assert last > first
    for page in reader.pages[first - 1 : last]:
        assert "Test Buffalo Sliders" in page.extract_text()
        if page.images:
            assert "Source:" in page.extract_text()
    assert any(d.code == "overflow" and d.path == source for d in result.diagnostics.warnings)
    with pytest.raises(ValidationFailed) as exc:
        build_cards(fixture_book, strict=True)
    assert any(d.code == "overflow" and d.path == source for d in exc.value.diagnostics.errors)
