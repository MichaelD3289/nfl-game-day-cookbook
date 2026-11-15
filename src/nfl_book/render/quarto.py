"""Compile generated QMD with Quarto and scan the LaTeX log for broken references."""

from __future__ import annotations

import re
import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from nfl_book.errors import Diagnostics, ValidationFailed

INSTALL_HINT = (
    "Install it (not done automatically):\n"
    "  brew install --cask quarto        # or the installer from https://quarto.org\n"
    "  quarto install tinytex            # LaTeX distribution used by Quarto"
)
LOG_LINES = 40

UNDEFINED_REF = re.compile(r"Reference `([^']+)' on page \d+ undefined")
MISSING_DEST = re.compile(r"name\{([^}]+)\} has been referenced but does not exist")


@dataclass(frozen=True)
class QuartoRun:
    returncode: int
    log: str  # standard output then standard error


class Quarto(Protocol):
    """Runs Quarto in a directory. Builds take one as a dependency; tests pass a fake."""

    def run(self, cwd: Path, args: Sequence[str]) -> QuartoRun | None:
        """Run ``quarto <args>`` in ``cwd``; ``None`` when Quarto is not installed."""
        ...


class QuartoCli:
    """The real thing: the ``quarto`` binary on PATH."""

    def run(self, cwd: Path, args: Sequence[str]) -> QuartoRun | None:
        quarto = shutil.which("quarto")
        if quarto is None:
            return None
        result = subprocess.run(
            [quarto, *args], cwd=cwd, capture_output=True, text=True, check=False
        )
        return QuartoRun(result.returncode, result.stdout + result.stderr)


def run_quarto(
    quarto: Quarto,
    cwd: Path,
    args: Sequence[str],
    *,
    source: Path,
    diagnostics: Diagnostics,
    code: str,
    what: str,
    skip: str,
    output: Path | None = None,
    log: Path | None = None,
) -> bool:
    """Run Quarto; report a missing binary, a failed render or a missing ``output`` as an
    error naming ``source`` (the document), with the end of Quarto's log. True on success."""
    result = quarto.run(cwd, args)
    if result is None:
        diagnostics.error(
            code,
            f"Quarto is required to build the {what} but was not found on PATH.\n"
            f"{INSTALL_HINT}\nOr run with {skip} to stop after generating the sources.",
            source,
        )
        return False
    tail = "\n".join(result.log.strip().splitlines()[-LOG_LINES:])
    where = f" (see {log})" if log is not None else ""
    if result.returncode != 0:
        diagnostics.error(code, f"Quarto {what} build failed{where}:\n{tail}", source)
        return False
    if output is not None and not output.is_file():
        diagnostics.error(
            code, f"Quarto finished but wrote no {output.name}{where}:\n{tail}", source
        )
        return False
    return True


def render_pdf(quarto: Quarto, document: Path, diagnostics: Diagnostics) -> Path:
    """Run ``quarto render`` in the document's directory; return the PDF path."""
    pdf = document.with_suffix(".pdf")
    ok = run_quarto(
        quarto,
        document.parent,
        ["render", document.name, "--to", "pdf"],
        source=document,
        diagnostics=diagnostics,
        code="quarto",
        what="PDF",
        skip="--no-pdf",
        output=pdf,
        log=document.with_suffix(".log"),
    )
    if not ok:
        raise ValidationFailed(diagnostics)
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
