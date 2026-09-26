from nfl_book.dependencies import DependencyGraph


def test_closure_is_transitive() -> None:
    graph = DependencyGraph({"a": ["b"], "b": ["c"], "c": [], "d": []})
    assert graph.closure(["a"]) == {"a", "b", "c"}
    assert graph.closure([]) == set()


def test_closure_ignores_unknown_nodes() -> None:
    graph = DependencyGraph({"a": ["missing"]})
    assert graph.closure(["a"]) == {"a", "missing"}


def test_acyclic_graph_has_no_cycles() -> None:
    assert DependencyGraph({"a": ["b", "c"], "b": ["c"], "c": []}).find_cycles() == []


def test_cycle_is_found() -> None:
    cycles = DependencyGraph({"a": ["b"], "b": ["c"], "c": ["a"]}).find_cycles()
    assert len(cycles) == 1
    cycle = cycles[0]
    assert cycle[0] == cycle[-1]
    assert set(cycle) == {"a", "b", "c"}


def test_self_reference_is_a_cycle() -> None:
    assert DependencyGraph({"a": ["a"]}).find_cycles() == [["a", "a"]]
