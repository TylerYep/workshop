from src.algorithms import johnsons_shortest_paths
from tests.algorithms.graph.all_pairs_shortest_path_test import TestShortestPaths


def test_johnsons() -> None:
    TestShortestPaths.all_test_scenarios(johnsons_shortest_paths)
