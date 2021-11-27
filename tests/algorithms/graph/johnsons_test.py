import pytest

from cs.algorithms import johnsons_shortest_paths
from tests.algorithms.graph.problems.apsp import AllPairsShortestPaths


@pytest.mark.add_function("shortest_paths_fn")
class TestJohnsons(AllPairsShortestPaths):
    shortest_paths_fn = johnsons_shortest_paths
