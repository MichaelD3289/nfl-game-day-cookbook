"""Discovery: paths define ownership; every error names its source file."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from nfl_book.config import load_settings
from nfl_book.discovery import discover
from nfl_book.errors import Diagnostics
from nfl_book.project import Project

Write = Callable[[str, str], Path]

RECIPE = """\
---
id: {id}
title: Probe
status: draft
course: sides
yield: 2 servings
{extra}---

## Ingredients

- 1 thing

## Instructions

Do it.
"""


def run(project: Project) -> tuple[Diagnostics, list[str]]:
    diags = Diagnostics()
    content = discover(project, load_settings(project), diags)
    return diags, sorted(r.id for r in content.recipes)


def messages_for(diags: Diagnostics, path: Path) -> list[str]:
    return [d.message for d in diags if d.path == path]


def test_fixture_book_discovers_cleanly(fixture_book: Project) -> None:
    diags, recipes = run(fixture_book)
    assert diags.errors == []
    assert recipes == ["test-buffalo-sliders", "test-citrus-wings", "test-draft-nachos"]


def test_team_comes_from_path(fixture_book: Project) -> None:
    content = discover(fixture_book, load_settings(fixture_book), Diagnostics())
    sliders = next(r for r in content.recipes if r.id == "test-buffalo-sliders")
    assert sliders.team.slug == "bills"
    assert sliders.division.key == "afc-east"


def test_unknown_team_directory(fixture_book: Project, write: Write) -> None:
    path = write("recipes/afc/east/cowboys/probe.md", RECIPE.format(id="probe", extra=""))
    diags, recipes = run(fixture_book)
    assert "probe" not in recipes
    assert any("'cowboys' is not in AFC East" in m for m in messages_for(diags, path))


def test_wrong_depth(fixture_book: Project, write: Write) -> None:
    path = write("recipes/afc/probe.md", RECIPE.format(id="probe", extra=""))
    diags, _ = run(fixture_book)
    assert [d.code for d in diags if d.path == path] == ["location"]


def test_id_must_match_file_name(fixture_book: Project, write: Write) -> None:
    path = write("recipes/afc/east/bills/probe.md", RECIPE.format(id="other", extra=""))
    diags, _ = run(fixture_book)
    assert any("must match the file name 'probe'" in m for m in messages_for(diags, path))


def test_team_field_is_forbidden(fixture_book: Project, write: Write) -> None:
    extra = "teams: [bills, jets]\n"
    path = write("recipes/afc/east/bills/probe.md", RECIPE.format(id="probe", extra=extra))
    diags, _ = run(fixture_book)
    assert any("ownership is inferred" in m for m in messages_for(diags, path))


def test_duplicate_ids_across_teams(fixture_book: Project, write: Write) -> None:
    a = write("recipes/afc/east/bills/probe.md", RECIPE.format(id="probe", extra=""))
    b = write("recipes/afc/east/jets/probe.md", RECIPE.format(id="probe", extra=""))
    diags, _ = run(fixture_book)
    duplicate = [d for d in diags if d.code == "duplicate-id"]
    assert duplicate, list(diags)
    assert {d.path for d in duplicate} & {a, b}


def test_marker_outside_ingredients(fixture_book: Project, write: Write) -> None:
    text = RECIPE.format(id="probe", extra="") + "Serve with {{component:test-wing-sauce}}.\n"
    path = write("recipes/afc/east/bills/probe.md", text)
    diags, _ = run(fixture_book)
    assert any("only allowed in '## Ingredients'" in m for m in messages_for(diags, path))


def test_unknown_section(fixture_book: Project, write: Write) -> None:
    text = RECIPE.format(id="probe", extra="") + "\n## Chef Secrets\n\nNope.\n"
    path = write("recipes/afc/east/bills/probe.md", text)
    diags, _ = run(fixture_book)
    assert any("unknown section '## Chef Secrets'" in m for m in messages_for(diags, path))


def test_bad_schema_value_names_file(fixture_book: Project, write: Write) -> None:
    text = RECIPE.format(id="probe", extra="").replace("status: draft", "status: maybe")
    path = write("recipes/afc/east/bills/probe.md", text)
    diags, _ = run(fixture_book)
    assert any(d.path == path and d.code == "schema" for d in diags), list(diags)


def test_component_kind_from_path(fixture_book: Project, write: Write) -> None:
    path = write(
        "components/gravies/probe.md",
        "---\nid: probe\ntitle: P\nstatus: draft\n---\n\n## Ingredients\n\n- x\n\n"
        "## From Scratch\n\nMix.\n",
    )
    diags, _ = run(fixture_book)
    assert any(d.path == path and d.code == "location" for d in diags), list(diags)


def test_tests_fixtures_are_not_in_production(empty_book: Project) -> None:
    diags, recipes = run(Project.create(empty_book.root))
    assert diags.errors == []
    assert not any(r.startswith("test-") for r in recipes)
