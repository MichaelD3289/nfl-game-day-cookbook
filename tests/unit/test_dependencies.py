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


def test_ordered_closure_is_depth_first_in_reference_order() -> None:
    graph = DependencyGraph({"a": ["c", "b"], "b": ["d"], "c": [], "d": [], "e": []})
    assert graph.ordered_closure(["a"]) == ("a", "c", "b", "d")
    assert graph.ordered_closure(["b", "a"]) == ("b", "d", "a", "c")
    assert graph.ordered_closure([]) == ()


def test_ordered_closure_lists_a_shared_child_once_at_first_use() -> None:
    graph = DependencyGraph({"a": ["s"], "b": ["s", "t"], "s": ["u"], "t": [], "u": []})
    assert graph.ordered_closure(["a", "b"]) == ("a", "s", "u", "b", "t")
    assert graph.ordered_closure(["a", "s"]) == ("a", "s", "u")


def test_ordered_closure_survives_cycles_and_unknown_nodes() -> None:
    graph = DependencyGraph({"a": ["b"], "b": ["c", "missing"], "c": ["a"]})
    assert graph.ordered_closure(["a"]) == ("a", "b", "c", "missing")
    assert DependencyGraph({"a": ["a"]}).ordered_closure(["a"]) == ("a",)
