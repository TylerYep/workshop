from src.algorithms import floyd_warshall_shortest_paths
from tests.algorithms.graph.all_pairs_shortest_path_test import TestShortestPaths


def test_floyd_warshall() -> None:
    TestShortestPaths.all_test_scenarios(floyd_warshall_shortest_paths)
