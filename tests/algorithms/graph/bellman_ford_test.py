from typing import Any

import pytest

from conftest import add_fixtures
from cs.algorithms import bellman_ford_shortest_paths
from cs.structures import Edge, Graph
from tests.algorithms.graph.problems.apsp import AllPairsShortestPaths


class TestFloydWarshall(AllPairsShortestPaths):
    shortest_paths_fn = AllPairsShortestPaths.single_source_to_all_pairs(
        bellman_ford_shortest_paths
    )

    @staticmethod
    def test_negative_cycles() -> None:
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
        graph2 = Graph.from_edgelist(
            [e01, e05, e12, e15, e23, e24, e43, e45, e51, e52],
            is_directed=False,
        )

        with pytest.raises(AssertionError):
            _ = bellman_ford_shortest_paths(graph2, 0)


def pytest_generate_tests(metafunc: Any) -> None:
    add_fixtures(metafunc, "shortest_paths_fn")
