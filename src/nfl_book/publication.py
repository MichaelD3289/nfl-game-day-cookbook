"""Who is in a build: the publication test, the component graph and its roots.

``resolve`` applies these once; everything downstream reads the resulting model.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

from nfl_book.dependencies import DependencyGraph
from nfl_book.models.common import Status
from nfl_book.models.content import Component, Recipe


def is_published(status: Status) -> bool:
    return status is Status.PUBLISHED


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
