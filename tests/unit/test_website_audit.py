"""The audit adapter preserves source diagnostics and fails execution errors."""

import json
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/website_audit.py"


@pytest.mark.parametrize("severity,code", [("warning", 0), ("error", 1)])
def test_adapter_reports_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    severity: str,
    code: int,
) -> None:
    report = tmp_path / "test-report.json"
    report.write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "severity": severity,
                        "code": "test-rule",
                        "source": "templates/test-source.qmd.j2",
                        "route": "recipe-test-fixture.html",
                        "message": "Synthetic finding",
                    }
                ]
            }
        )
    )
    monkeypatch.setattr(sys, "argv", [str(SCRIPT), str(tmp_path), "--report", str(report)])
    monkeypatch.setattr(subprocess, "run", Mock(return_value=subprocess.CompletedProcess([], code)))
    assert runpy.run_path(str(SCRIPT))["main"]() == code
    output = capsys.readouterr().out
    assert "templates/test-source.qmd.j2" in output
    assert "recipe-test-fixture.html" in output
    assert "Synthetic finding" in output


@pytest.mark.parametrize(
    "failure", [OSError("Missing node"), subprocess.TimeoutExpired("node", 900)]
)
def test_adapter_execution_errors_fail(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: Exception,
) -> None:
    monkeypatch.setattr(
        sys, "argv", [str(SCRIPT), str(tmp_path), "--report", str(tmp_path / "test-report.json")]
    )
    monkeypatch.setattr(subprocess, "run", Mock(side_effect=failure))
    assert runpy.run_path(str(SCRIPT))["main"]() == 1
    assert "scripts/website-audit.js: error" in capsys.readouterr().out
