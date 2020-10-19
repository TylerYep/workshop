import pytest

from src.algorithms import bellman_ford
from src.structures import Edge, Graph


def test_bellman_ford_adj_list() -> None:
    graph = Graph[str](
        {
            "a": {"b": -1, "c": 4},
            "b": {"c": 3, "d": 2, "e": 2},
            "c": {},
            "d": {"b": 1, "c": 5},
            "e": {"d": -3},
        }
    )

    assert bellman_ford(graph, "a") == {"a": 0, "b": -1, "c": 2, "d": -2, "e": 1}

    graph = Graph[str](
        {
            "S": {"A": 6},
            "A": {"B": 3},
            "B": {"C": 4, "E": 5},
            "C": {"A": -3, "D": 3},
            "D": {},
            "E": {},
        }
    )

    assert bellman_ford(graph, "S") == {
        "S": 0,
        "A": 6,
        "B": 9,
        "C": 13,
        "D": 16,
        "E": 14,
    }


def test_bellman_ford_edge_list() -> None:
    e01 = Edge(0, 1, -1)
    e05 = Edge(0, 5, 2)
    e12 = Edge(1, 2, 2)
    e15 = Edge(1, 5, -2)
    e23 = Edge(2, 3, 5)
    e24 = Edge(2, 4, 1)
    e43 = Edge(4, 3, -4)
    e45 = Edge(4, 5, 3)
    e51 = Edge(5, 1, 2)
    e52 = Edge(5, 2, 3)
    graph = Graph.from_edgelist([e01, e05, e12, e15, e23, e24, e43, e45, e51, e52])

    assert bellman_ford(graph, 0) == {0: 0, 1: -1, 2: 0, 3: -3, 4: 1, 5: -3}

    graph2 = Graph.from_edgelist(
        [e01, e05, e12, e15, e23, e24, e43, e45, e51, e52],
        is_directed=False,
    )

    with pytest.raises(AssertionError):
        _ = bellman_ford(graph2, 0)
