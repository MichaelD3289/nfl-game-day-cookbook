"""The recipe catalog (``recipes.json``): one JSON description of every published recipe.

The website's Browse recipes page filters by its facets, and later site features
(search, planners, shopping lists) can read the same file instead of scraping pages.
Facets come from ``data/indexes.yml`` first, in file order, then the league facets
(conference, division, team). Nothing here is hard-coded per index, so a new index
becomes a new filter without code changes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nfl_book.errors import Diagnostics
from nfl_book.models.content import Recipe
from nfl_book.references import recipe_label
from nfl_book.render.pages import PageSpec
from nfl_book.resolve import BookModel
from nfl_book.validation import LEAGUE_FACETS, component_graph

__all__ = ["CATALOG_FILE", "CATALOG_VERSION", "LEAGUE_FACETS", "recipe_catalog", "write_catalog"]

CATALOG_FILE = "recipes.json"
CATALOG_VERSION = 1
INDEX_TITLE_PREFIX = "Index by "


def _facet_title(title: str) -> str:
    return title[len(INDEX_TITLE_PREFIX) :] if title.startswith(INDEX_TITLE_PREFIX) else title


def _index_facets(model: BookModel) -> list[dict[str, Any]]:
    return [
        {
            "id": index.definition.id,
            "title": _facet_title(index.definition.title),
            "source": "index",
            "options": [{"id": b.id, "label": b.label} for b in index.definition.config.buckets],
        }
        for index in model.indexes
    ]


def _league_facets(model: BookModel) -> list[dict[str, Any]]:
    conferences: dict[str, str] = {}
    divisions: list[dict[str, str]] = []
    teams: list[dict[str, str]] = []
    for section in model.divisions:
        division = section.division
        published = [t.team for t in section.teams if t.recipes]
        if not published:
            continue
        conferences.setdefault(division.conference_id, division.conference_name)
        divisions.append({"id": division.key, "label": division.name})
        teams += [{"id": t.slug, "label": t.name, "group": division.name} for t in published]
    options = {
        "conference": [{"id": k, "label": v} for k, v in conferences.items()],
        "division": divisions,
        "team": teams,
    }
    titles = {"conference": "Conference", "division": "Division", "team": "Team"}
    return [
        {"id": fid, "title": titles[fid], "source": "league", "options": options[fid]}
        for fid in LEAGUE_FACETS
    ]


def _recipe_entry(
    model: BookModel,
    recipe: Recipe,
    page: PageSpec,
    components: tuple[str, ...],
) -> dict[str, Any]:
    meta = recipe.meta
    course = model.settings.course(meta.course)
    facets: dict[str, list[str]] = {}
    for index in model.indexes:
        known = index.definition.bucket_ids
        facets[index.definition.id] = [
            b for b in index.definition.buckets_for(recipe) if b in known
        ]
    facets["conference"] = [recipe.division.conference_id]
    facets["division"] = [recipe.division.key]
    facets["team"] = [recipe.team.slug]
    servings = recipe.servings
    return {
        "id": recipe.id,
        "title": recipe.title,
        "url": f"{page.slug}.html",
        "photo": page.context.get("image") or None,
        "photo_size": page.context.get("image_size", 0),
        "description": meta.description or "",
        "course": meta.course,
        "course_label": course.singular if course else meta.course,
        "team": {
            "slug": recipe.team.slug,
            "name": recipe.team.name,
            "short_name": recipe.team.short_name,
            "abbreviation": recipe.team.abbreviation,
        },
        "location": recipe.location,
        "conference": recipe.division.conference_id,
        "division": recipe.division.key,
        "division_name": recipe.division.name,
        "servings": list(servings) if servings else None,
        "yield": meta.yield_,
        "prep": meta.prep,
        "cook": meta.cook,
        "components": list(components),
        "facets": facets,
    }


def recipe_catalog(
    model: BookModel, pages: list[PageSpec], diags: Diagnostics, *, edition: str
) -> dict[str, Any]:
    """The catalog of ``model`` (already filtered to published content) in book order.

    ``pages`` supplies each recipe's page slug and web photo. A recipe without a page
    is reported against its source file and left out.
    """
    by_label = {label: page for page in pages for label in page.anchors}
    graph = component_graph(model.components)
    published = {c.id for c in model.components}
    recipes = []
    for recipe in model.recipes:
        page = by_label.get(recipe_label(recipe.id))
        if page is None:
            diags.error("catalog", "recipe has no website page for the catalog", recipe.path)
            continue
        closure = graph.ordered_closure(recipe.component_refs)
        components = tuple(cid for cid in closure if cid in published)
        recipes.append(_recipe_entry(model, recipe, page, components))
    return {
        "version": CATALOG_VERSION,
        "edition": edition,
        "facets": _index_facets(model) + _league_facets(model),
        "recipes": recipes,
    }


def write_catalog(catalog: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
