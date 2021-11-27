from typing import Any

from cs.algorithms import johnsons_shortest_paths
from tests.algorithms.graph.problems.apsp import AllPairsShortestPaths
from tests.conftest import add_fixtures


class TestJohnsons(AllPairsShortestPaths):
    shortest_paths_fn = johnsons_shortest_paths


def pytest_generate_tests(metafunc: Any) -> None:
    add_fixtures(metafunc, "shortest_paths_fn")
