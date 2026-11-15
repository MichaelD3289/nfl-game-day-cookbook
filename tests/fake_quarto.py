"""A stand-in for the Quarto runner, so post-render paths run without Quarto installed."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

from nfl_book.render.quarto import QuartoRun


class FakeQuarto:
    """Records each call, optionally writes the files Quarto would have written."""

    def __init__(
        self,
        *,
        installed: bool = True,
        returncode: int = 0,
        log: str = "",
        writes: Callable[[Path, Sequence[str]], None] | None = None,
    ) -> None:
        self.installed = installed
        self.returncode = returncode
        self.log = log
        self.writes = writes
        self.calls: list[tuple[Path, tuple[str, ...]]] = []

    def run(self, cwd: Path, args: Sequence[str]) -> QuartoRun | None:
        self.calls.append((cwd, tuple(args)))
        if not self.installed:
            return None
        if self.writes is not None:
            self.writes(cwd, args)
        return QuartoRun(self.returncode, self.log)
