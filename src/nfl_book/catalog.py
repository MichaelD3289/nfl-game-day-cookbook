"""The recipe catalog (``recipes.json``): one JSON description of every published recipe.

The website's Browse recipes page filters by its facets, and later site features
(search, planners) can read the same file instead of scraping pages.
Facets come from ``data/indexes.yml`` first, in file order, then the league facets
(conference, division, team). Nothing here is hard-coded per index, so a new index
becomes a new filter without code changes.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nfl_book.indexes import LEAGUE_FACETS
from nfl_book.models.content import Recipe
from nfl_book.references import address, recipe_label
from nfl_book.render.pages import Media
from nfl_book.resolve import BookModel

__all__ = [
    "CATALOG_FILE",
    "CATALOG_VERSION",
    "LEAGUE_FACETS",
    "Catalog",
    "CatalogFacet",
    "CatalogOption",
    "CatalogRecipe",
    "CatalogTeam",
    "recipe_catalog",
    "write_catalog",
]

CATALOG_FILE = "recipes.json"
CATALOG_VERSION = 1
INDEX_TITLE_PREFIX = "Index by "


@dataclass(frozen=True)
class CatalogOption:
    id: str
    label: str
    group: str | None = None  # team options: the division they are listed under

    def as_dict(self) -> dict[str, str]:
        found = {"id": self.id, "label": self.label}
        if self.group is not None:
            found["group"] = self.group
        return found


@dataclass(frozen=True)
class CatalogFacet:
    id: str
    title: str
    source: str  # "index" or "league"
    options: tuple[CatalogOption, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "options": [o.as_dict() for o in self.options],
        }


@dataclass(frozen=True)
class CatalogTeam:
    slug: str
    name: str
    short_name: str
    abbreviation: str

    def as_dict(self) -> dict[str, str]:
        return {
            "slug": self.slug,
            "name": self.name,
            "short_name": self.short_name,
            "abbreviation": self.abbreviation,
        }


@dataclass(frozen=True)
class CatalogRecipe:
    id: str
    title: str
    url: str
    photo: str | None
    photo_size: int
    description: str
    course: str
    course_label: str
    team: CatalogTeam
    location: str
    conference: str
    division: str
    division_name: str
    servings: tuple[int, int] | None
    yield_: str | None
    prep: str | None
    cook: str | None
    components: tuple[str, ...]
    facets: Mapping[str, tuple[str, ...]]

    @property
    def facets_json(self) -> str:
        """The facets as the JSON the finder pages put in a ``data-facets`` attribute."""
        return json.dumps(self.facets, ensure_ascii=False)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "photo": self.photo,
            "photo_size": self.photo_size,
            "description": self.description,
            "course": self.course,
            "course_label": self.course_label,
            "team": self.team.as_dict(),
            "location": self.location,
            "conference": self.conference,
            "division": self.division,
            "division_name": self.division_name,
            "servings": list(self.servings) if self.servings else None,
            "yield": self.yield_,
            "prep": self.prep,
            "cook": self.cook,
            "components": list(self.components),
            "facets": {k: list(v) for k, v in self.facets.items()},
        }


@dataclass(frozen=True)
class Catalog:
    edition: str
    facets: tuple[CatalogFacet, ...]
    recipes: tuple[CatalogRecipe, ...]

    def facet(self, facet_id: str) -> CatalogFacet:
        return next(f for f in self.facets if f.id == facet_id)

    def as_dict(self) -> dict[str, Any]:
        return {
            "version": CATALOG_VERSION,
            "edition": self.edition,
            "facets": [f.as_dict() for f in self.facets],
            "recipes": [r.as_dict() for r in self.recipes],
        }


def _facet_title(title: str) -> str:
    return title[len(INDEX_TITLE_PREFIX) :] if title.startswith(INDEX_TITLE_PREFIX) else title


def _index_facets(model: BookModel) -> list[CatalogFacet]:
    return [
        CatalogFacet(
            index.definition.id,
            _facet_title(index.definition.title),
            "index",
            tuple(CatalogOption(b.id, b.label) for b in index.definition.config.buckets),
        )
        for index in model.indexes
    ]


def _league_facets(model: BookModel) -> list[CatalogFacet]:
    conferences: dict[str, str] = {}
    divisions: list[CatalogOption] = []
    teams: list[CatalogOption] = []
    for section in model.divisions:
        division = section.division
        published = [t.team for t in section.teams if t.recipes]
        if not published:
            continue
        conferences.setdefault(division.conference_id, division.conference_name)
        divisions.append(CatalogOption(division.key, division.name))
        teams += [CatalogOption(t.slug, t.name, division.name) for t in published]
    options = {
        "conference": [CatalogOption(k, v) for k, v in conferences.items()],
        "division": divisions,
        "team": teams,
    }
    titles = {"conference": "Conference", "division": "Division", "team": "Team"}
    return [CatalogFacet(fid, titles[fid], "league", tuple(options[fid])) for fid in LEAGUE_FACETS]


def _recipe_entry(model: BookModel, recipe: Recipe, media: Media) -> CatalogRecipe:
    meta = recipe.meta
    course = model.settings.course(meta.course)
    facets: dict[str, tuple[str, ...]] = {}
    for index in model.indexes:
        known = index.definition.bucket_ids
        facets[index.definition.id] = tuple(
            b for b in index.definition.buckets_for(recipe) if b in known
        )
    facets["conference"] = (recipe.division.conference_id,)
    facets["division"] = (recipe.division.key,)
    facets["team"] = (recipe.team.slug,)
    servings = recipe.servings
    label = recipe_label(recipe.id)
    return CatalogRecipe(
        id=recipe.id,
        title=recipe.title,
        url=address(recipe).page_url,
        photo=media.images.get(label) or None,
        photo_size=media.image_sizes.get(label, 0),
        description=meta.description or "",
        course=meta.course,
        course_label=course.singular if course else meta.course,
        team=CatalogTeam(
            recipe.team.slug, recipe.team.name, recipe.team.short_name, recipe.team.abbreviation
        ),
        location=recipe.location,
        conference=recipe.division.conference_id,
        division=recipe.division.key,
        division_name=recipe.division.name,
        servings=(servings[0], servings[1]) if servings else None,
        yield_=meta.yield_,
        prep=meta.prep,
        cook=meta.cook,
        components=tuple(c.id for c in model.components_for(recipe)),
        facets=facets,
    )


def recipe_catalog(model: BookModel, media: Media, *, edition: str) -> Catalog:
    """The catalog of ``model`` (already filtered to published content) in book order.

    ``media`` supplies each recipe's web photo.
    """
    return Catalog(
        edition=edition,
        facets=tuple(_index_facets(model) + _league_facets(model)),
        recipes=tuple(_recipe_entry(model, recipe, media) for recipe in model.recipes),
    )


def write_catalog(catalog: Catalog, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(catalog.as_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
