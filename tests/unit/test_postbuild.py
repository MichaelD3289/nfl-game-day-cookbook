from __future__ import annotations

import json
from pathlib import Path

from nfl_book.errors import Diagnostics
from nfl_book.postbuild import check_manifest, load_pagemap, write_pagemap
from nfl_book.render.quarto import scan_log


def manifest(tmp_path: Path) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps(
            {
                "pages": [
                    {
                        "file": "pages/001-recipe-a.qmd",
                        "anchors": ["recipe:a", "recipe:a:end"],
                        "spans": [["recipe:a", "recipe:a:end"]],
                    }
                ]
            }
        )
    )
    return path


def test_all_anchors_on_one_page(tmp_path: Path) -> None:
    diags = Diagnostics()
    assert (
        check_manifest(manifest(tmp_path), {"recipe:a": 5, "recipe:a:end": 5}, diags, strict=True)
        == []
    )
    assert diags.ok and len(diags) == 0


def test_missing_anchor_is_an_error(tmp_path: Path) -> None:
    diags = Diagnostics()
    check_manifest(manifest(tmp_path), {"recipe:a": 5}, diags, strict=False)
    assert [d.code for d in diags.errors] == ["anchor"]
    assert diags.errors[0].path == tmp_path / "pages/001-recipe-a.qmd"


def test_overflow_warns_or_fails(tmp_path: Path) -> None:
    pagemap = {"recipe:a": 5, "recipe:a:end": 6}
    lenient = Diagnostics()
    overflows = check_manifest(manifest(tmp_path), pagemap, lenient, strict=False)
    assert [(o.first, o.last) for o in overflows] == [(5, 6)]
    assert lenient.ok and [d.code for d in lenient.warnings] == ["overflow"]
    strict = Diagnostics()
    check_manifest(manifest(tmp_path), pagemap, strict, strict=True)
    assert [d.code for d in strict.errors] == ["overflow"]


def test_pagemap_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "pagemap.json"
    write_pagemap({"recipe:b": 2, "recipe:a": 1}, path)
    assert load_pagemap(path) == {"recipe:a": 1, "recipe:b": 2}
    assert load_pagemap(tmp_path / "missing.json") == {}


def test_scan_log_finds_wrapped_undefined_reference(tmp_path: Path) -> None:
    log = tmp_path / "book.log"
    log.write_text(
        "LaTeX Warning: Reference `component:test-wing-sau\nce' on page 7 undefined"
        " on input line 1.\n"
    )
    diags = Diagnostics()
    scan_log(log, diags)
    assert [d.message for d in diags.errors] == [
        "LaTeX reference to undefined label 'component:test-wing-sauce'"
    ]
