"""The only network stage: fill the shortlink cache for non-retired sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from nfl_book.models.common import Status
from nfl_book.models.content import Component, Content, Recipe
from nfl_book.shortlinks.cache import ShortlinkCache
from nfl_book.shortlinks.providers import Shortener


@dataclass
class PrepareResult:
    added: dict[str, str] = field(default_factory=dict)
    cached: int = 0
    changed: bool = False


def sources_to_check(content: Content) -> dict[str, tuple[Path, ...]]:
    """Every non-retired source URL (drafts too) with the files that cite it.

    URLs keep first-seen order; each URL's files are sorted and unique.
    """
    urls: dict[str, set[Path]] = {}
    items: list[Recipe | Component] = [*content.recipes, *content.components]
    for item in items:
        if item.meta.status is not Status.RETIRED and item.meta.source:
            urls.setdefault(item.meta.source.url, set()).add(item.path)
    return {url: tuple(sorted(files)) for url, files in urls.items()}


def urls_to_prepare(content: Content) -> list[str]:
    """Every non-retired source URL (drafts too, so they are ready when published)."""
    return list(sources_to_check(content))


def prepare_shortlinks(
    content: Content, cache: ShortlinkCache, shortener: Shortener
) -> PrepareResult:
    result = PrepareResult()
    for url in urls_to_prepare(content):
        if url in cache:
            result.cached += 1
            continue
        short = shortener.shorten(url)
        cache.add(url, short)
        result.added[url] = short
    if result.added:
        result.changed = cache.save()
    return result
