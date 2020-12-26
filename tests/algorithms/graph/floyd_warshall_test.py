from src.algorithms import floyd_warshall_shortest_paths
from tests.algorithms.graph.problems.all_pairs_shortest_paths import TestShortestPaths


def test_floyd_warshall() -> None:
    TestShortestPaths.all_test_scenarios(floyd_warshall_shortest_paths)
