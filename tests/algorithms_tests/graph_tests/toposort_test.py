import pytest

from src.algorithms import topological_sort
from src.structures import Graph


def test_topological_sort() -> None:
    """
    Ordered from bottom to top
        a
       / \
      b   c
     / \
    d   e
    """
    graph: Graph[str] = Graph.from_iterable(
        {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
    )
    assert topological_sort(graph) == ["c", "d", "e", "b", "a"]

    graph = Graph.from_iterable({"a": ["c"], "b": ["d"], "c": ["d"], "d": []})
    assert topological_sort(graph) == ["d", "c", "a", "b"]

    graph2: Graph[int] = Graph.from_iterable(
        {1: [2, 3], 2: [4, 5, 6], 3: [4, 6], 4: [5, 6], 5: [6], 6: []}
    )
    assert topological_sort(graph2) == [6, 5, 4, 2, 3, 1]

    graph2 = Graph.from_iterable({1: [3], 3: [5, 6], 5: [4], 4: [7], 7: [], 6: []})
    assert topological_sort(graph2) == [7, 4, 5, 6, 3, 1]


def test_topological_sort_cycle_detection() -> None:
    graph: Graph[str] = Graph.from_iterable({"a": ["a"]})
    with pytest.raises(ValueError):
        _ = topological_sort(graph)

    graph = Graph.from_iterable({"a": ["b"], "b": ["c"], "c": ["a"]})
    with pytest.raises(ValueError):
        _ = topological_sort(graph)
