from typing import Any

import pytest

from conftest import add_fixtures
from cs.algorithms import dijkstra_search, dijkstra_shortest_paths
from cs.structures import Graph
from tests.algorithms.graph.problems.apsp import AllPairsShortestPaths, APSPFunction


class TestDijkstras(AllPairsShortestPaths):
    shortest_paths_fn = AllPairsShortestPaths.single_source_to_all_pairs(
        dijkstra_shortest_paths
    )

    def test_adj_list_neg_weights(self, shortest_paths_fn: APSPFunction[Any]) -> None:
        graph = Graph[str](
            {
                "a": {"b": -1, "c": 4},
                "b": {"c": 3, "d": 2, "e": 2},
                "c": {},
                "d": {"b": 1, "c": 5},
                "e": {"d": -3},
            }
        )
        with pytest.raises(RuntimeError):
            _ = shortest_paths_fn(graph)

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

        with pytest.raises(RuntimeError):
            _ = shortest_paths_fn(graph)


def pytest_generate_tests(metafunc: Any) -> None:
    add_fixtures(metafunc, "shortest_paths_fn")


def test_dijkstra_search() -> None:
    G = Graph[str](
        {
            "A": {"B": 2, "C": 5},
            "B": {"A": 2, "D": 3, "E": 1, "F": 1},
            "C": {"A": 5, "F": 3},
            "D": {"B": 3},
            "E": {"B": 4, "F": 3},
            "F": {"C": 3, "E": 3},
        }
    )

    G2 = Graph[int]({2: {3: 1}, 3: {4: 1}, 4: {6: 1}, 5: {2: 1, 6: 3}, 6: {}})

    G3 = Graph[str](
        {
            "B": {"C": 1},
            "C": {"D": 1},
            "D": {"F": 1},
            "E": {"B": 1, "G": 2},
            "F": {},
            "G": {"F": 1},
        }
    )

    assert dijkstra_search(G, "E", "C") == 6
    assert dijkstra_search(G2, 5, 6) == 3
    assert dijkstra_search(G3, "E", "F") == 3

    r"""
    Layout of G2:
    E -- (1) --> B -- (1) --> C
    |                         |
    (3)                       (1)
    \                       /
        F <-- (1) --- D  <--
    """

    r"""
    Layout of G3:
    E -- 1 --> B -- 1 --> C -- 1 --> D -- 1 --> F
    \                                         /\
    \                                        ||
        -------- 2 ---------> G ------- 1 ------
    """
