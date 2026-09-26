"""The declarative ``field`` index kind: buckets read from recipe front matter."""

from __future__ import annotations

from nfl_book.indexes.base import IndexDefinition, register_index_kind
from nfl_book.models.config import IndexConfig
from nfl_book.models.content import Recipe

INDEX_PREFIX = "index."


@register_index_kind("field")
class FieldIndex(IndexDefinition):
    """``field: course`` reads a top-level key; ``field: index.<key>`` reads the index map."""

    def __init__(self, config: IndexConfig) -> None:
        super().__init__(config)
        if not config.field:
            raise ValueError(f"index {config.id!r}: kind 'field' requires `field`")
        self.field = config.field

    def front_matter_keys(self) -> set[str]:
        if self.field.startswith(INDEX_PREFIX):
            return {self.field.removeprefix(INDEX_PREFIX)}
        return set()

    def _raw(self, recipe: Recipe) -> object:
        if self.field.startswith(INDEX_PREFIX):
            return recipe.meta.index.get(self.field.removeprefix(INDEX_PREFIX))
        return getattr(recipe.meta, self.field, None)

    def buckets_for(self, recipe: Recipe) -> list[str]:
        value = self._raw(recipe)
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v) for v in value]
        return [str(value)]

    def validate(self, recipe: Recipe, *, published: bool = True) -> list[str]:
        problems = super().validate(recipe, published=published)
        if isinstance(self._raw(recipe), list) and not self.config.multiple:
            problems.append(f"{self.id}: takes a single value, not a list")
        return problems
