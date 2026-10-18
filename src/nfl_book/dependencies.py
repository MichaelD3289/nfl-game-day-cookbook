"""Component dependency graph.

Edges run from a recipe or component to each component it references. A
component is included in a build iff it is reachable from a published recipe
(or is published with ``always_include: true``). Cycles between components are
rejected.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence


class DependencyGraph:
    def __init__(self, edges: Mapping[str, Sequence[str]]) -> None:
        """``edges`` maps a component id to the component ids it references, in the
        order they are referenced (kept for ``ordered_closure``)."""
        self.edges = {k: tuple(v) for k, v in edges.items()}

    def find_cycles(self) -> list[list[str]]:
        """Each cycle as a closed path, e.g. ``["a", "b", "a"]`` (deterministic)."""
        cycles: list[list[str]] = []
        seen_cycles: set[frozenset[str]] = set()
        state: dict[str, int] = {}  # 1 = on stack, 2 = done
        stack: list[str] = []

        def visit(node: str) -> None:
            state[node] = 1
            stack.append(node)
            for dep in self.edges.get(node, ()):
                if state.get(dep) == 1:
                    cycle = [*stack[stack.index(dep) :], dep]
                    key = frozenset(cycle)
                    if key not in seen_cycles:
                        seen_cycles.add(key)
                        cycles.append(cycle)
                elif dep not in state:
                    visit(dep)
            stack.pop()
            state[node] = 2

        for node in sorted(self.edges):
            if node not in state:
                visit(node)
        return cycles

    def closure(self, roots: Iterable[str]) -> set[str]:
        """All components reachable from ``roots`` (roots themselves included)."""
        result: set[str] = set()
        pending = list(roots)
        while pending:
            node = pending.pop()
            if node in result:
                continue
            result.add(node)
            pending.extend(self.edges.get(node, ()))
        return result

    def ordered_closure(self, roots: Sequence[str]) -> tuple[str, ...]:
        """``closure`` in depth-first preorder: each root, then what it references in
        reference order, each id once at its first occurrence. Cycles are cut short."""
        result: dict[str, None] = {}

        def visit(node: str) -> None:
            if node in result:
                return
            result[node] = None
            for dep in self.edges.get(node, ()):
                visit(dep)

        for root in roots:
            visit(root)
        return tuple(result)
