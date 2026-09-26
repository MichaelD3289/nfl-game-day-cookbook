"""Diagnostics shared by every pipeline stage.

Every problem found while loading or validating content becomes a
:class:`Diagnostic` that names the offending source file, so authors and
agents can go straight to the file that needs fixing.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    path: Path | None = None
    severity: Severity = Severity.ERROR

    def format(self, root: Path | None = None) -> str:
        location = ""
        if self.path is not None:
            shown = self.path
            if root is not None:
                try:
                    shown = self.path.resolve().relative_to(root.resolve())
                except ValueError:
                    shown = self.path
            location = f"{shown}: "
        return f"{location}{self.severity.value} [{self.code}] {self.message}"


@dataclass
class Diagnostics:
    items: list[Diagnostic] = field(default_factory=list)

    def error(self, code: str, message: str, path: Path | None = None) -> None:
        self.items.append(Diagnostic(code, message, path, Severity.ERROR))

    def warning(self, code: str, message: str, path: Path | None = None) -> None:
        self.items.append(Diagnostic(code, message, path, Severity.WARNING))

    def extend(self, other: Iterable[Diagnostic]) -> None:
        self.items.extend(other)

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.items if d.severity is Severity.ERROR]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [d for d in self.items if d.severity is Severity.WARNING]

    @property
    def ok(self) -> bool:
        return not self.errors

    def codes(self) -> set[str]:
        return {d.code for d in self.items}

    def for_paths(self, paths: Iterable[Path]) -> Diagnostics:
        wanted = {p.resolve() for p in paths}
        return Diagnostics([d for d in self.items if d.path and d.path.resolve() in wanted])

    def __iter__(self) -> Iterator[Diagnostic]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)


class BookError(Exception):
    """A pipeline stage cannot continue."""


class ValidationFailed(BookError):
    def __init__(self, diagnostics: Diagnostics) -> None:
        self.diagnostics = diagnostics
        super().__init__(f"{len(diagnostics.errors)} validation error(s)")
