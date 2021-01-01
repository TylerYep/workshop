from typing import Any

from conftest import add_fixtures
from cs.algorithms import johnsons_shortest_paths
from tests.algorithms.graph.problems.apsp import AllPairsShortestPaths


class TestJohnsons(AllPairsShortestPaths):
    shortest_paths_fn = johnsons_shortest_paths


def pytest_generate_tests(metafunc: Any) -> None:
    add_fixtures(metafunc, "shortest_paths_fn")
