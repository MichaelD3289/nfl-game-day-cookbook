"""Create draft recipe/component files in the right place. Never overwrites."""

from __future__ import annotations

from pathlib import Path

from nfl_book.config import Settings
from nfl_book.errors import BookError
from nfl_book.indexes import build_index
from nfl_book.project import Project
from nfl_book.references import SLUG_RE
from nfl_book.render.env import make_env


def _check_slug(slug: str) -> None:
    if not SLUG_RE.fullmatch(slug):
        raise BookError(f"invalid slug {slug!r}: use lowercase letters, digits and hyphens")


def _title(slug: str) -> str:
    return slug.replace("-", " ").title()


def _write_new(path: Path, text: str) -> Path:
    if path.exists():
        raise BookError(f"{path} already exists; refusing to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _check_unique_id(project: Project, slug: str, base: Path) -> None:
    clash = next((p for p in base.rglob(f"{slug}.md")), None) if base.is_dir() else None
    if clash is not None:
        raise BookError(f"id {slug!r} already used by {clash}")


def new_recipe(project: Project, settings: Settings, team_slug: str, slug: str) -> Path:
    _check_slug(slug)
    found = settings.league.team(team_slug)
    if found is None:
        known = ", ".join(t.slug for t in settings.league.teams)
        raise BookError(f"unknown team {team_slug!r} (known: {known})")
    division, _ = found
    _check_unique_id(project, slug, project.recipes_dir)
    index_keys = []
    for config in settings.indexes:
        index_keys.extend(sorted(build_index(config).front_matter_keys()))
    text = (
        make_env(project.templates_dir)
        .get_template("scaffold/recipe.md.j2")
        .render(
            id=slug,
            title=_title(slug),
            course=settings.course_index.buckets[0].id,
            index_keys=index_keys,
        )
    )
    path = project.recipes_dir / division.conference_id / division.id / team_slug / f"{slug}.md"
    return _write_new(path, text)


def new_component(project: Project, settings: Settings, kind_id: str, slug: str) -> Path:
    _check_slug(slug)
    kind = settings.component_kind(kind_id)
    if kind is None:
        known = ", ".join(k.id for k in settings.component_kinds)
        raise BookError(f"unknown component kind {kind_id!r} (known: {known})")
    _check_unique_id(project, slug, project.components_dir)
    text = (
        make_env(project.templates_dir)
        .get_template("scaffold/component.md.j2")
        .render(id=slug, title=_title(slug))
    )
    return _write_new(project.components_dir / kind.id / f"{slug}.md", text)
