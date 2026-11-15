"""Configurable recipe indexes.

Indexes are declared in ``data/indexes.yml``. The built-in ``field`` kind
covers front-matter-driven indexes; register new computed kinds with
:func:`register_index_kind` and reference them by ``kind:``.
"""

from nfl_book.indexes import field as _field  # noqa: F401  (registers "field")
from nfl_book.indexes.base import (
    IndexDefinition,
    IndexSection,
    build_index,
    index_kinds,
    register_index_kind,
)

# Filter ids the website catalog adds after the indexes; an index may not reuse them.
LEAGUE_FACETS = ("conference", "division", "team")

__all__ = [
    "LEAGUE_FACETS",
    "IndexDefinition",
    "IndexSection",
    "build_index",
    "index_kinds",
    "register_index_kind",
]
