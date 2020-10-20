from src.algorithms import bellman_ford_shortest_paths
from tests.algorithms.graph.all_pairs_shortest_path_test import TestShortestPaths


def test_bellman_ford_adj_list() -> None:
    TestShortestPaths.all_test_scenarios(
        TestShortestPaths.single_source_to_all_pairs(bellman_ford_shortest_paths)
    )
    TestShortestPaths.negative_cycles(bellman_ford_shortest_paths)
