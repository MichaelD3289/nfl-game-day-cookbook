"""Index framework: an index maps each published recipe to zero or more buckets."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from nfl_book.models.config import Bucket, IndexConfig
from nfl_book.models.content import Recipe


@dataclass(frozen=True)
class IndexSection:
    bucket: Bucket
    recipes: tuple[Recipe, ...]


class IndexDefinition(ABC):
    """Base class for index kinds. Subclasses decide which buckets a recipe is in."""

    def __init__(self, config: IndexConfig) -> None:
        self.config = config
        self.bucket_ids = [b.id for b in config.buckets]

    @property
    def id(self) -> str:
        return self.config.id

    @property
    def title(self) -> str:
        return self.config.title

    def front_matter_keys(self) -> set[str]:
        """Keys under the recipe's ``index:`` mapping this definition consumes."""
        return set()

    @abstractmethod
    def buckets_for(self, recipe: Recipe) -> list[str]:
        """Bucket ids the recipe belongs to (may contain unknown ids; see ``validate``)."""

    def validate(self, recipe: Recipe, *, published: bool = True) -> list[str]:
        """Problems with this recipe for this index (empty when fine).

        Unknown bucket ids are always errors; missing required values only
        matter for published recipes, so drafts can be filled in gradually.
        """
        problems = []
        buckets = self.buckets_for(recipe)
        for bucket in buckets:
            if bucket not in self.bucket_ids:
                allowed = ", ".join(self.bucket_ids)
                problems.append(f"{self.id}: unknown bucket {bucket!r} (allowed: {allowed})")
        if published and self.config.required and not buckets:
            problems.append(f"{self.id}: a value is required for published recipes")
        return problems

    def sections(self, recipes: Sequence[Recipe]) -> list[IndexSection]:
        """Group recipes (already in book order) by bucket, sorted by title within a bucket."""
        result = []
        for bucket in self.config.buckets:
            members = [r for r in recipes if bucket.id in self.buckets_for(r)]
            members.sort(key=lambda r: (r.title.casefold(), r.id))
            result.append(IndexSection(bucket, tuple(members)))
        return result


IndexFactory = Callable[[IndexConfig], IndexDefinition]
_REGISTRY: dict[str, type[IndexDefinition]] = {}


def register_index_kind(
    kind: str,
) -> Callable[[type[IndexDefinition]], type[IndexDefinition]]:
    """Class decorator registering an index kind usable from ``data/indexes.yml``."""

    def decorate(cls: type[IndexDefinition]) -> type[IndexDefinition]:
        if kind in _REGISTRY and _REGISTRY[kind] is not cls:
            raise ValueError(f"index kind {kind!r} is already registered")
        _REGISTRY[kind] = cls
        return cls

    return decorate


def index_kinds() -> dict[str, type[IndexDefinition]]:
    return dict(_REGISTRY)


def build_index(config: IndexConfig) -> IndexDefinition:
    try:
        cls = _REGISTRY[config.kind]
    except KeyError:
        known = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"unknown index kind {config.kind!r} (known: {known})") from None
    return cls(config)
