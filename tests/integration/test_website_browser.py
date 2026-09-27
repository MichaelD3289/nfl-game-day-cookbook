"""Real-browser checks always render a temporary synthetic sample-book."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from nfl_book.project import Project
from nfl_book.qr import qr_png
from nfl_book.website import build_website

REPO = Path(__file__).resolve().parents[2]


@pytest.mark.skipif(
    os.environ.get("NFL_BROWSER_TESTS") != "1",
    reason="opt in with NFL_BROWSER_TESTS=1 (requires npm ci and Chromium)",
)
def test_synthetic_website_browser_audit(fixture_book: Project, tmp_path: Path) -> None:
    assert shutil.which("quarto"), "Quarto is required for browser checks"
    config = fixture_book.data_dir / "book.yml"
    data = yaml.safe_load(config.read_text())
    data["suggestion_form_url"] = "https://example.invalid/test-suggestions"
    config.write_text(yaml.safe_dump(data))
    recipe = next(fixture_book.recipes_dir.rglob("test-buffalo-sliders.md"))
    recipe.write_text(
        recipe.read_text().replace(
            "status: published",
            "status: published\nimage: test-photo.png\nphoto_credit: Synthetic fixture",
        )
    )
    (recipe.parent / "test-photo.png").write_bytes(qr_png("https://example.invalid/test-photo"))
    result = build_website(fixture_book)
    report = tmp_path / "audit.json"
    completed = subprocess.run(
        ["node", str(REPO / "scripts/website-audit.js"), str(result.site), str(report)],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=240,
    )
    if report.exists() and (destination := os.environ.get("NFL_BROWSER_REPORTS")):
        report_dir = Path(destination)
        report_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(report, report_dir / "synthetic-accessibility.json")
    assert report.exists(), completed.stderr
    findings = json.loads(report.read_text())
    assert completed.returncode == 0, findings
    assert {r["kind"] for r in findings["routes"]} == {
        "home",
        "recipe",
        "component",
        "menu",
        "dishoff",
        "index",
        "versions",
    }
    assert findings["blockedRequests"] == []

    assert {"scaling", "quick-options", "suggestion", "print"} <= set(findings["coverage"])
