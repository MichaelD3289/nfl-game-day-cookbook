"""Division publication output stays independent of the full book."""

import json
import re
from unittest.mock import patch

from nfl_book import pipeline
from nfl_book.config import load_settings
from nfl_book.project import Project


def test_selected_cover_metadata_and_manifest(fixture_book: Project) -> None:
    cover = fixture_book.content_root / "book/frontmatter/cover.md"
    cover.write_text("---\ntitle: Fixture Cookbook\n---\n90 recipes, 32 teams, 8 divisions.\n")
    full = pipeline.build(fixture_book, pdf=False)
    original = full.document.read_bytes()
    result = pipeline.build(fixture_book, pdf=False, division="afc/east")
    assert result.document == fixture_book.generated_dir / "booklets/afc-east/book/book.qmd"
    assert "AFC East" in result.document.read_text()
    texts = "\n".join(p.read_text() for p in result.document.parent.glob("pages/*.qmd"))
    assert "2 recipes from 2 teams" in texts
    assert "90 recipes" not in texts
    assert "32 teams" not in texts
    assert "test-draft" not in texts
    assert "division:nfc-" not in texts
    manifest = json.loads((result.document.parent / "manifest.json").read_text())
    anchors = {a for p in manifest["pages"] for a in p["anchors"]}
    refs = set(re.findall(r"\\(?:BookPageRef|ComponentRef|DishOffRecipe)\{([^}]+)\}", texts))
    assert refs <= anchors
    assert full.document.read_bytes() == original


def test_booklets_builds_each_configured_division_once(fixture_book: Project) -> None:
    expected = load_settings(fixture_book).league.divisions
    with patch("nfl_book.pipeline.build", wraps=pipeline.build) as build:
        results = pipeline.build_booklets(fixture_book, pdf=False, strict=True)
    assert len(results) == len(expected) == 8
    assert [c.kwargs for c in build.call_args_list] == [
        {"pdf": False, "strict": True, "division": f"{d.conference_id}/{d.id}"} for d in expected
    ]
    assert len({r.document for r in results}) == 8
    empty = next(r for r in results if "nfc-north" in str(r.document))
    assert (
        "0 recipes from 0 teams"
        in next(empty.document.parent.glob("pages/*-cover.qmd")).read_text()
    )


def test_selected_pdf_destination_and_pagemap(fixture_book: Project) -> None:
    compiled = fixture_book.content_root / "test.pdf"
    compiled.write_bytes(b"test PDF")
    with (
        patch("nfl_book.pipeline.render_pdf", return_value=compiled),
        patch("nfl_book.pipeline.read_pagemap", return_value={}),
        patch("nfl_book.pipeline.check_manifest", return_value=[]),
    ):
        result = pipeline.build(fixture_book, division="afc/east")
    assert result.pdf == fixture_book.dist_dir / "nfl-game-day-recipe-booklet-afc-east.pdf"
    assert result.pdf.read_bytes() == compiled.read_bytes()
    assert (fixture_book.generated_dir / "booklets/afc-east/pagemap.json").is_file()
    assert not fixture_book.pagemap_file.exists()
