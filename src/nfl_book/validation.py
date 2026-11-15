"""Cross-document validation: references, indexes, dependencies, shortlinks, review age."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from PIL import Image

from nfl_book.config import Settings
from nfl_book.errors import Diagnostics
from nfl_book.indexes import LEAGUE_FACETS, IndexDefinition, build_index
from nfl_book.models.content import Component, Content, Recipe
from nfl_book.photo_prepare import (
    MAX_BYTES,
    MAX_EDGE,
    POLICY_VERSION,
    PhotoPreparationError,
    parse_photo_manifest,
)
from nfl_book.publication import component_graph, is_published, publication_roots
from nfl_book.reviews import check_review_ages
from nfl_book.shortlinks import ShortlinkCache


def build_indexes(settings: Settings, diags: Diagnostics, path: Path) -> list[IndexDefinition]:
    result = []
    for config in settings.indexes:
        if config.id in LEAGUE_FACETS:
            reserved = ", ".join(LEAGUE_FACETS)
            diags.error(
                "config",
                f"index id {config.id!r} is reserved for the website's league filters "
                f"({reserved}); choose another id",
                path,
            )
            continue
        try:
            result.append(build_index(config))
        except ValueError as exc:
            diags.error("config", str(exc), path)
    return result


def validate_content(
    settings: Settings,
    content: Content,
    shortlinks: ShortlinkCache,
    diags: Diagnostics,
    *,
    indexes_path: Path,
    content_root: Path,
    photo_manifest_path: Path,
    require_shortlinks: bool,
    today: date | None = None,
) -> None:
    indexes = build_indexes(settings, diags, indexes_path)
    photo_manifest = _load_photo_manifest(photo_manifest_path, diags)
    components = {c.id: c for c in content.components}
    recipes = {r.id: r for r in content.recipes}

    for recipe in content.recipes:
        _validate_recipe(recipe, indexes, components, diags)
        _validate_photo_preparation(recipe, content_root, photo_manifest, diags)
    for component in content.components:
        _validate_component(component, components, diags)
    _validate_duplicates(content.recipes, diags)
    _validate_graph(content, components, diags)
    _validate_menus(content, recipes, diags)
    _validate_shortlinks(content, shortlinks, diags, require_shortlinks)
    check_review_ages(content, settings.book.review_max_age_days, diags, today)


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
    if published and not recipe.meta.image:
        diags.warning("photo", "published recipe has no photo", path)
    if recipe.meta.image and not (path.parent / recipe.meta.image).is_file():
        diags.error("asset", f"image not found: {recipe.meta.image}", path)
    _check_ingredient_groups(recipe, diags)


def _load_photo_manifest(path: Path, diags: Diagnostics) -> dict[str, tuple[str, int]] | None:
    """Load the optional preparation manifest; malformed data is a named diagnostic."""
    if not path.exists():
        return {}
    try:
        entries = parse_photo_manifest(path.read_bytes(), path)
    except OSError as exc:
        diags.error("photo-manifest", f"cannot read photo manifest: {exc}", path)
        return None
    except PhotoPreparationError as exc:
        diags.error("photo-manifest", str(exc), path)
        return None
    return {key: (entry["sha256"], entry["policy"]) for key, entry in entries.items()}


def _validate_photo_preparation(
    recipe: Recipe,
    content_root: Path,
    manifest: dict[str, tuple[str, int]] | None,
    diags: Diagnostics,
) -> None:
    """Warn when a recipe image is absent or stale in the preparation manifest."""
    if not recipe.meta.image:
        return
    source = recipe.path.parent / recipe.meta.image
    if not source.is_file():
        return  # _validate_recipe already reports the missing referenced asset.

    reasons: list[str] = []
    suffix = source.suffix.casefold()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        diags.warning(
            "photo-preparation",
            f"unsupported source format {suffix or '(no extension)'}; supported formats are "
            ".jpg, .jpeg, .png, or .webp",
            recipe.path,
        )
        return
    try:
        key = source.resolve().relative_to(content_root.resolve()).as_posix()
    except ValueError:
        key = ""
        reasons.append("image path is outside the content root")

    if not key:
        diags.warning(
            "photo-preparation",
            "photo is outside the content root; update the recipe image path",
            recipe.path,
        )
        return

    recorded = manifest.get(key) if manifest is not None else None
    if recorded is None:
        reasons.append("image is not listed in data/photo-manifest.yml")
    else:
        expected_hash, policy = recorded
        try:
            actual_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        except OSError:
            reasons.append("image bytes could not be checked")
        else:
            if actual_hash != expected_hash:
                reasons.append("manifest hash is stale")
        if policy != POLICY_VERSION:
            reasons.append(
                f"policy version is stale (manifest says {policy}, expected {POLICY_VERSION})"
            )

    try:
        with Image.open(source) as image:
            if image.format != "WEBP" or source.suffix.casefold() != ".webp":
                reasons.append("image is not in WebP format")
            if max(image.size) > MAX_EDGE:
                reasons.append(f"image exceeds the {MAX_EDGE} px edge limit")
    except (OSError, SyntaxError, ValueError, Image.DecompressionBombError):
        reasons.append("image is not a readable WebP")

    try:
        if source.stat().st_size > MAX_BYTES:
            reasons.append(f"image exceeds {MAX_BYTES // 1024} KB")
    except OSError:
        reasons.append("image size could not be checked")

    if reasons:
        detail = "; ".join(reasons)
        diags.warning(
            "photo-preparation",
            f"photo needs preparation ({detail}); "
            + (
                "repair data/photo-manifest.yml before running validation"
                if manifest is None
                else "run `nfl-book prepare-photos`"
            ),
            recipe.path,
        )


def _check_ingredient_groups(recipe: Recipe, diags: Diagnostics) -> None:
    """Warn when one ``###`` group holds every ingredient.

    That usually means the main ingredients were left under a sub-recipe heading
    (a sauce or salad listed first), because a group runs until the next heading.
    """
    groups = recipe.ingredients
    if len(groups) == 1 and groups[0].heading is not None:
        diags.warning(
            "ingredients",
            f"ingredient group {groups[0].heading!r} holds every ingredient; give each "
            "part of the dish its own '###' group, or remove the heading",
            recipe.path,
        )


def _title_key(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.casefold()))


def _validate_duplicates(recipes: Sequence[Recipe], diags: Diagnostics) -> None:
    """Warn when published recipes share a title or a source URL.

    Teams that share a city each get their own local dishes, so the same dish on
    two teams is a duplicate to resolve (see the update-recipe skill).
    """
    seen: dict[tuple[str, str], Recipe] = {}
    for recipe in recipes:
        if not is_published(recipe.meta.status):
            continue
        keys = [("title", _title_key(recipe.title))]
        if recipe.meta.source:
            keys.append(("source", recipe.meta.source.url.strip().rstrip("/")))
        for kind, value in keys:
            other = seen.setdefault((kind, value), recipe)
            if other is recipe:
                continue
            for here, there in ((recipe, other), (other, recipe)):
                diags.warning(
                    "duplicate",
                    f"same {kind} as {there.path.name} ({there.team.name}); keep one "
                    "and give the other team a different local dish",
                    here.path,
                )


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
