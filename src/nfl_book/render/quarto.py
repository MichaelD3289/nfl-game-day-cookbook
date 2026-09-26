"""Compile generated QMD with Quarto and scan the LaTeX log for broken references."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from nfl_book.errors import BookError, Diagnostics

INSTALL_HINT = (
    "Quarto is required to compile the PDF but was not found on PATH.\n"
    "Install it (not done automatically):\n"
    "  brew install --cask quarto        # or the installer from https://quarto.org\n"
    "  quarto install tinytex            # LaTeX distribution used by Quarto\n"
    "Or run with --no-pdf to stop after generating QMD."
)

UNDEFINED_REF = re.compile(r"Reference `([^']+)' on page \d+ undefined")
MISSING_DEST = re.compile(r"name\{([^}]+)\} has been referenced but does not exist")


def find_quarto() -> str:
    quarto = shutil.which("quarto")
    if quarto is None:
        raise BookError(INSTALL_HINT)
    return quarto


def render_pdf(document: Path) -> Path:
    """Run ``quarto render`` in the document's directory; return the PDF path."""
    quarto = find_quarto()
    result = subprocess.run(
        [quarto, "render", document.name, "--to", "pdf"],
        cwd=document.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    pdf = document.with_suffix(".pdf")
    if result.returncode != 0 or not pdf.is_file():
        tail = "\n".join((result.stdout + result.stderr).strip().splitlines()[-40:])
        log = document.with_suffix(".log")
        raise BookError(f"quarto render failed (see {log}):\n{tail}")
    return pdf


def scan_log(log: Path, diags: Diagnostics) -> None:
    """Undefined references mean a label was referenced but never anchored."""
    if not log.is_file():
        diags.warning("latex", f"LaTeX log not found at {log}; reference check skipped")
        return
    text = log.read_text(encoding="utf-8", errors="replace")
    joined = text.replace("\n", "")  # pdfTeX wraps long log lines at 79 chars
    missing = sorted(set(UNDEFINED_REF.findall(joined)) | set(MISSING_DEST.findall(joined)))
    for label in missing:
        diags.error("reference", f"LaTeX reference to undefined label {label!r}", log)
    if not missing and "There were undefined references" in joined:
        diags.error("reference", "LaTeX reported undefined references", log)
