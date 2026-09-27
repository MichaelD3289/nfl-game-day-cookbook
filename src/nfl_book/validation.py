"""Cross-document validation: references, indexes, dependencies, shortlinks."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from pathlib import Path

from nfl_book.config import Settings
from nfl_book.dependencies import DependencyGraph
from nfl_book.errors import Diagnostics
from nfl_book.indexes import IndexDefinition, build_index
from nfl_book.models.common import Status
from nfl_book.models.content import Component, Content, Recipe
from nfl_book.shortlinks import ShortlinkCache


def is_published(status: Status) -> bool:
    return status is Status.PUBLISHED


def build_indexes(settings: Settings, diags: Diagnostics, path: Path) -> list[IndexDefinition]:
    result = []
    for config in settings.indexes:
        try:
            result.append(build_index(config))
        except ValueError as exc:
            diags.error("config", str(exc), path)
    return result


def component_graph(components: Sequence[Component]) -> DependencyGraph:
    return DependencyGraph({c.id: c.component_refs for c in components})


def publication_roots(
    recipes: Iterable[Recipe],
    components: Iterable[Component],
    include: Callable[[Status], bool],
) -> set[str]:
    """Components a book must contain before following dependencies.

    Those referenced by included recipes, plus included ``always_include``
    components (whose own dependencies must be printed too).
    """
    roots = {ref for r in recipes if include(r.meta.status) for ref in r.component_refs}
    roots |= {c.id for c in components if include(c.meta.status) and c.meta.always_include}
    return roots


def validate_content(
    settings: Settings,
    content: Content,
    shortlinks: ShortlinkCache,
    diags: Diagnostics,
    *,
    indexes_path: Path,
    require_shortlinks: bool,
) -> None:
    indexes = build_indexes(settings, diags, indexes_path)
    components = {c.id: c for c in content.components}
    recipes = {r.id: r for r in content.recipes}

    for recipe in content.recipes:
        _validate_recipe(recipe, indexes, components, diags)
    for component in content.components:
        _validate_component(component, components, diags)
    _validate_graph(content, components, diags)
    _validate_menus(content, recipes, diags)
    _validate_shortlinks(content, shortlinks, diags, require_shortlinks)


def _validate_recipe(
    recipe: Recipe,
    indexes: list[IndexDefinition],
    components: dict[str, Component],
    diags: Diagnostics,
) -> None:
    path = recipe.path
    published = is_published(recipe.meta.status)
    for index in indexes:
        for problem in index.validate(recipe, published=published):
            diags.error("index", problem, path)
    known_keys = set().union(*(i.front_matter_keys() for i in indexes))
    for key in recipe.meta.index:
        if key not in known_keys:
            allowed = ", ".join(sorted(known_keys)) or "none"
            diags.error("index", f"index.{key}: unknown index key (allowed: {allowed})", path)
    _check_refs(recipe.component_refs, published, components, path, diags)
    for key in recipe.meta.quick_options:
        if key not in recipe.component_refs:
            diags.error(
                "reference",
                f"quick_options.{key}: component is not referenced in '## Ingredients'",
                path,
            )
    if recipe.meta.image and not (path.parent / recipe.meta.image).is_file():
        diags.error("asset", f"image not found: {recipe.meta.image}", path)


def _check_refs(
    refs: Sequence[str],
    published: bool,
    components: dict[str, Component],
    path: Path,
    diags: Diagnostics,
) -> None:
    for ref in refs:
        target = components.get(ref)
        if target is None:
            diags.error("reference", f"unknown component {ref!r}", path)
        elif published and not is_published(target.meta.status):
            diags.error(
                "reference",
                f"published content references component {ref!r} "
                f"whose status is {target.meta.status.value}",
                path,
            )


def _validate_component(
    component: Component, components: dict[str, Component], diags: Diagnostics
) -> None:
    published = is_published(component.meta.status)
    _check_refs(component.component_refs, published, components, component.path, diags)


def _validate_graph(content: Content, components: dict[str, Component], diags: Diagnostics) -> None:
    graph = component_graph(content.components)
    for cycle in graph.find_cycles():
        diags.error(
            "cycle",
            "component dependency cycle: " + " -> ".join(cycle),
            components[cycle[0]].path,
        )
    reachable = graph.closure(publication_roots(content.recipes, content.components, is_published))
    for component in content.components:
        if (
            is_published(component.meta.status)
            and not component.meta.always_include
            and component.id not in reachable
        ):
            diags.warning(
                "unused",
                "published component is not used by any published recipe and will be omitted "
                "(set always_include: true to keep it)",
                component.path,
            )


def _validate_menus(content: Content, recipes: dict[str, Recipe], diags: Diagnostics) -> None:
    items = [
        (m.path, m.meta.status, m.meta.recipes, m.meta.timeline, None) for m in content.menus
    ] + [
        (d.path, d.meta.status, d.meta.recipes, d.meta.timeline, d.division)
        for d in content.dishoffs
    ]
    for path, status, recipe_ids, timeline, division in items:
        for n, step in enumerate(timeline or ()):
            if step.recipe is not None and step.recipe not in recipe_ids:
                diags.error(
                    "reference",
                    f"timeline.{n}.recipe: {step.recipe!r} is not one of this menu's recipes",
                    path,
                )
        seen: set[str] = set()
        for rid in recipe_ids:
            if rid in seen:
                diags.error("reference", f"recipe {rid!r} is listed more than once", path)
            seen.add(rid)
            recipe = recipes.get(rid)
            if recipe is None:
                diags.error("reference", f"unknown recipe {rid!r}", path)
                continue
            if is_published(status) and not is_published(recipe.meta.status):
                diags.error(
                    "reference",
                    f"recipe {rid!r} is {recipe.meta.status.value}; "
                    "published menus may only list published recipes",
                    path,
                )
            if division is not None and recipe.division.key != division.key:
                diags.error(
                    "reference",
                    f"recipe {rid!r} belongs to {recipe.division.name}, not {division.name}",
                    path,
                )


def _validate_shortlinks(
    content: Content,
    shortlinks: ShortlinkCache,
    diags: Diagnostics,
    required: bool,
) -> None:
    for url, path in published_source_urls(content):
        if url not in shortlinks:
            message = (
                f"no short URL cached for {url}; run `uv run nfl-book prepare-links` "
                "(requires network) and commit data/shortlinks.yml"
            )
            if required:
                diags.error("shortlink", message, path)
            else:
                diags.warning("shortlink", message, path)


def published_source_urls(content: Content) -> list[tuple[str, Path]]:
    """Source URLs of published content that can appear in a production build."""
    urls = []
    items: list[Recipe | Component] = [*content.recipes, *content.components]
    for item in items:
        if is_published(item.meta.status) and item.meta.source:
            urls.append((item.meta.source.url, item.path))
    return urls
