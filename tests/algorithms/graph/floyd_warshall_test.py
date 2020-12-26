from typing import Any

from conftest import add_fixtures
from src.algorithms import floyd_warshall_shortest_paths
from tests.algorithms.graph.problems.apsp import AllPairsShortestPaths


class TestFloydWarshall(AllPairsShortestPaths):
    shortest_paths_fn = floyd_warshall_shortest_paths


def pytest_generate_tests(metafunc: Any) -> None:
    add_fixtures(metafunc, "shortest_paths_fn")
