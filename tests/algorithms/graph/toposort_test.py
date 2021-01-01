import pytest

from cs.algorithms import topological_sort
from cs.structures import Graph


def test_topological_sort() -> None:
    """
    Ordered from bottom to top
        a
       / \
      b   c
     / \
    d   e
    """
    graph = Graph[str]({"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []})
    assert topological_sort(graph) == ["c", "d", "e", "b", "a"]

    graph = Graph({"a": ["c"], "b": ["d"], "c": ["d"], "d": []})
    assert topological_sort(graph) == ["d", "c", "a", "b"]

    graph2 = Graph[int]({1: [2, 3], 2: [4, 5, 6], 3: [4, 6], 4: [5, 6], 5: [6], 6: []})
    assert topological_sort(graph2) == [6, 5, 4, 2, 3, 1]

    graph2 = Graph({1: [3], 3: [5, 6], 5: [4], 4: [7], 7: [], 6: []})
    assert topological_sort(graph2) == [7, 4, 5, 6, 3, 1]


def test_topological_sort_cycle_detection() -> None:
    graph = Graph[str]({"a": ["a"]})
    with pytest.raises(ValueError, match="Cycle detected in node a"):
        _ = topological_sort(graph)

    graph = Graph({"a": ["b"], "b": ["c"], "c": ["a"]})
    with pytest.raises(ValueError, match="Cycle detected in node c"):
        _ = topological_sort(graph)
