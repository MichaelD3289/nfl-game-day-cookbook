"""Load and validate the authored configuration under ``data/``."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

import yaml
from pydantic import BaseModel, ValidationError

from nfl_book.errors import Diagnostics, ValidationFailed
from nfl_book.models.config import (
    BookConfig,
    Bucket,
    ComponentKind,
    ComponentKindsFile,
    IndexConfig,
    IndexesFile,
    MenuType,
    MenuTypesFile,
)
from nfl_book.models.nfl import League
from nfl_book.project import Project

M = TypeVar("M", bound=BaseModel)


class YamlError(Exception):
    pass


def read_yaml(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except FileNotFoundError as exc:
        raise YamlError("file not found") from exc
    except yaml.YAMLError as exc:
        raise YamlError(f"invalid YAML: {exc}") from exc


def format_validation_error(exc: ValidationError) -> list[str]:
    """Turn a pydantic error into short ``field: message`` lines."""
    lines = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err["loc"]) or "(document)"
        msg = err["msg"].removeprefix("Value error, ")
        if err["type"] == "extra_forbidden":
            msg = "unknown field"
        lines.append(f"{loc}: {msg}")
    return lines


def load_model(path: Path, model: type[M], diagnostics: Diagnostics, code: str) -> M | None:
    try:
        data = read_yaml(path)
    except YamlError as exc:
        diagnostics.error(code, str(exc), path)
        return None
    try:
        return model.model_validate(data if data is not None else {})
    except ValidationError as exc:
        for line in format_validation_error(exc):
            diagnostics.error(code, line, path)
        return None


@dataclass(frozen=True)
class Settings:
    """All authored configuration, validated."""

    book: BookConfig
    league: League
    indexes: tuple[IndexConfig, ...]
    menu_types: tuple[MenuType, ...]
    component_kinds: tuple[ComponentKind, ...]

    @property
    def course_index(self) -> IndexConfig:
        return next(i for i in self.indexes if i.id == "course")

    def course(self, course_id: str) -> Bucket | None:
        return next((b for b in self.course_index.buckets if b.id == course_id), None)

    def menu_type(self, type_id: str) -> MenuType | None:
        return next((m for m in self.menu_types if m.id == type_id), None)

    def component_kind(self, kind_id: str) -> ComponentKind | None:
        return next((k for k in self.component_kinds if k.id == kind_id), None)


def load_settings(project: Project) -> Settings:
    """Load ``data/*.yml``; raise :class:`ValidationFailed` naming the bad file."""
    diags = Diagnostics()
    data = project.data_dir
    book = load_model(data / "book.yml", BookConfig, diags, "config")
    league = load_model(data / "nfl.yml", League, diags, "config")
    indexes = load_model(data / "indexes.yml", IndexesFile, diags, "config")
    menu_types = load_model(data / "menu-types.yml", MenuTypesFile, diags, "config")
    kinds = load_model(data / "component-kinds.yml", ComponentKindsFile, diags, "config")
    if not diags.ok or not (book and league and indexes and menu_types and kinds):
        raise ValidationFailed(diags)
    return Settings(
        book=book,
        league=league,
        indexes=tuple(indexes.indexes),
        menu_types=tuple(menu_types.menu_types),
        component_kinds=tuple(kinds.component_kinds),
    )
