"""Find and parse authored content.

Ownership is inferred from location:

* ``recipes/<conference>/<division>/<team>/<recipe-id>.md`` -> exactly one team
* ``components/<kind>/<component-id>.md``
* ``menus/game-day/<menu-type>/<menu-id>.yml``
* ``menus/divisions/<conference>/<division>/<dish-off-id>.yml``

Files and directories whose names start with ``.`` or ``_`` are ignored, as
are non-Markdown files beside recipes (e.g. photos). Every problem becomes a
diagnostic naming the source file; discovery never stops at the first error.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypeVar

from pydantic import ValidationError

from nfl_book.config import Settings, YamlError, format_validation_error, read_yaml
from nfl_book.errors import Diagnostics
from nfl_book.markdown import DocumentError, read_document, split_sections
from nfl_book.models.config import CoverMeta
from nfl_book.models.content import (
    Component,
    ComponentMeta,
    Content,
    CoverPage,
    DishOff,
    DishOffMeta,
    GameDayMenu,
    GameDayMenuMeta,
    IngredientGroup,
    Recipe,
    RecipeMeta,
)
from nfl_book.project import Project
from nfl_book.references import find_markers, parse_ingredients

T = TypeVar("T", RecipeMeta, ComponentMeta, GameDayMenuMeta, DishOffMeta)

RECIPE_SECTIONS = {"Ingredients": True, "Instructions": True, "Kitchen Notes": False}
COMPONENT_SECTIONS = {"Ingredients": True, "From Scratch": True, "Note": False}


def iter_files(base: Path, suffixes: tuple[str, ...]) -> Iterator[Path]:
    if not base.is_dir():
        return
    for path in sorted(base.rglob("*")):
        rel = path.relative_to(base)
        if any(part.startswith((".", "_")) for part in rel.parts):
            continue
        if path.is_file() and path.suffix in suffixes:
            yield path


def discover(project: Project, settings: Settings, diags: Diagnostics) -> Content:
    content = Content(
        recipes=list(_recipes(project, settings, diags)),
        components=list(_components(project, settings, diags)),
        menus=list(_menus(project, settings, diags)),
        dishoffs=list(_dishoffs(project, settings, diags)),
        cover=_cover(project, diags),
    )
    for kind, items in (
        ("recipe", content.recipes),
        ("component", content.components),
        ("menu", content.menus),
        ("dish-off", content.dishoffs),
    ):
        _check_unique(kind, [(i.id, i.path) for i in items], diags)
    return content


def _check_unique(kind: str, items: list[tuple[str, Path]], diags: Diagnostics) -> None:
    seen: dict[str, Path] = {}
    for item_id, path in items:
        if item_id in seen:
            diags.error(
                "duplicate-id",
                f"{kind} id {item_id!r} is already used by {seen[item_id]}",
                path,
            )
        else:
            seen[item_id] = path


def _validate_meta(
    model: type[T], data: dict[str, Any], path: Path, diags: Diagnostics
) -> T | None:
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        for line in format_validation_error(exc):
            diags.error("schema", line, path)
        return None


def _check_id(meta_id: str, path: Path, diags: Diagnostics) -> bool:
    if meta_id != path.stem:
        diags.error("id-mismatch", f"id {meta_id!r} must match the file name {path.stem!r}", path)
        return False
    return True


def _sections(
    body: str, spec: dict[str, bool], path: Path, diags: Diagnostics
) -> dict[str, str] | None:
    preamble, sections, duplicates = split_sections(body)
    ok = True
    if preamble:
        diags.error("structure", "text before the first '## ' section heading", path)
        ok = False
    for title in duplicates:
        diags.error("structure", f"section '## {title}' appears more than once", path)
        ok = False
    for title in sections:
        if title not in spec:
            allowed = ", ".join(f"'## {s}'" for s in spec)
            diags.error("structure", f"unknown section '## {title}' (allowed: {allowed})", path)
            ok = False
    for title, required in spec.items():
        if required and not sections.get(title):
            diags.error("structure", f"missing required section '## {title}'", path)
            ok = False
    for title, text in sections.items():
        if title != "Ingredients" and find_markers(text):
            diags.error(
                "reference",
                "component references are only allowed in '## Ingredients' "
                f"(found in '## {title}')",
                path,
            )
            ok = False
    return sections if ok else None


def _ingredients(text: str, path: Path, diags: Diagnostics) -> tuple[IngredientGroup, ...] | None:
    groups, problems = parse_ingredients(text)
    for problem in problems:
        diags.error("ingredients", problem, path)
    return None if problems else groups


def _recipes(project: Project, settings: Settings, diags: Diagnostics) -> Iterator[Recipe]:
    base = project.recipes_dir
    for path in iter_files(base, (".md",)):
        parts = path.relative_to(base).parts
        if len(parts) != 4:
            diags.error(
                "location",
                "recipes must live at recipes/<conference>/<division>/<team>/<recipe-id>.md",
                path,
            )
            continue
        conf, div, team_slug, _ = parts
        division = settings.league.division(conf, div)
        if division is None:
            diags.error("location", f"unknown division {conf}/{div} (see data/nfl.yml)", path)
            continue
        team = next((t for t in division.teams if t.slug == team_slug), None)
        if team is None:
            diags.error(
                "location", f"team {team_slug!r} is not in {division.name} (see data/nfl.yml)", path
            )
            continue
        try:
            doc = read_document(path)
        except DocumentError as exc:
            diags.error("parse", str(exc), path)
            continue
        for forbidden in ("team", "division", "conference", "teams"):
            if forbidden in doc.meta:
                diags.error(
                    "schema",
                    f"{forbidden}: ownership is inferred from the directory; remove this field",
                    path,
                )
                doc.meta.pop(forbidden)
        meta = _validate_meta(RecipeMeta, doc.meta, path, diags)
        sections = _sections(doc.body, RECIPE_SECTIONS, path, diags)
        if meta is None or sections is None or not _check_id(meta.id, path, diags):
            continue
        groups = _ingredients(sections["Ingredients"], path, diags)
        if groups is None:
            continue
        yield Recipe(
            meta=meta,
            path=path,
            division=division,
            team=team,
            ingredients=groups,
            instructions=sections["Instructions"],
            kitchen_notes=sections.get("Kitchen Notes") or None,
        )


def _components(project: Project, settings: Settings, diags: Diagnostics) -> Iterator[Component]:
    base = project.components_dir
    for path in iter_files(base, (".md",)):
        parts = path.relative_to(base).parts
        if len(parts) != 2:
            diags.error(
                "location", "components must live at components/<kind>/<component-id>.md", path
            )
            continue
        kind = settings.component_kind(parts[0])
        if kind is None:
            diags.error(
                "location",
                f"unknown component kind {parts[0]!r} (see data/component-kinds.yml)",
                path,
            )
            continue
        try:
            doc = read_document(path)
        except DocumentError as exc:
            diags.error("parse", str(exc), path)
            continue
        meta = _validate_meta(ComponentMeta, doc.meta, path, diags)
        sections = _sections(doc.body, COMPONENT_SECTIONS, path, diags)
        if meta is None or sections is None or not _check_id(meta.id, path, diags):
            continue
        groups = _ingredients(sections["Ingredients"], path, diags)
        if groups is None:
            continue
        yield Component(
            meta=meta,
            path=path,
            kind=kind,
            ingredients=groups,
            method=sections["From Scratch"],
            note=sections.get("Note") or None,
        )


def _load_yaml_mapping(path: Path, diags: Diagnostics) -> dict[str, Any] | None:
    try:
        data = read_yaml(path)
    except YamlError as exc:
        diags.error("parse", str(exc), path)
        return None
    if not isinstance(data, dict):
        diags.error("parse", "file must contain a YAML mapping", path)
        return None
    return data


def _menus(project: Project, settings: Settings, diags: Diagnostics) -> Iterator[GameDayMenu]:
    base = project.game_day_dir
    for path in iter_files(base, (".yml", ".yaml")):
        parts = path.relative_to(base).parts
        if len(parts) != 2:
            diags.error(
                "location", "menus must live at menus/game-day/<menu-type>/<menu-id>.yml", path
            )
            continue
        menu_type = settings.menu_type(parts[0])
        if menu_type is None:
            diags.error(
                "location", f"unknown menu type {parts[0]!r} (see data/menu-types.yml)", path
            )
            continue
        data = _load_yaml_mapping(path, diags)
        meta = data and _validate_meta(GameDayMenuMeta, data, path, diags)
        if meta and _check_id(meta.id, path, diags):
            yield GameDayMenu(meta=meta, path=path, menu_type=menu_type)


def _dishoffs(project: Project, settings: Settings, diags: Diagnostics) -> Iterator[DishOff]:
    base = project.dishoffs_dir
    for path in iter_files(base, (".yml", ".yaml")):
        parts = path.relative_to(base).parts
        if len(parts) != 3:
            diags.error(
                "location",
                "dish-offs must live at menus/divisions/<conference>/<division>/<id>.yml",
                path,
            )
            continue
        division = settings.league.division(parts[0], parts[1])
        if division is None:
            diags.error(
                "location", f"unknown division {parts[0]}/{parts[1]} (see data/nfl.yml)", path
            )
            continue
        data = _load_yaml_mapping(path, diags)
        meta = data and _validate_meta(DishOffMeta, data, path, diags)
        if meta and _check_id(meta.id, path, diags):
            yield DishOff(meta=meta, path=path, division=division)


def _cover(project: Project, diags: Diagnostics) -> CoverPage | None:
    path = project.frontmatter_dir / "cover.md"
    if not path.is_file():
        return None
    try:
        doc = read_document(path)
        meta = CoverMeta.model_validate(doc.meta)
    except DocumentError as exc:
        diags.error("parse", str(exc), path)
        return None
    except ValidationError as exc:
        for line in format_validation_error(exc):
            diags.error("schema", line, path)
        return None
    return CoverPage(
        title=meta.title or "",
        subtitle=meta.subtitle,
        tagline=meta.tagline,
        body=doc.body.strip(),
    )
