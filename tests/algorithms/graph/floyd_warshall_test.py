import pytest

from cs.algorithms import floyd_warshall_shortest_paths
from tests.algorithms.graph.problems.apsp import AllPairsShortestPaths


@pytest.mark.add_function("shortest_paths_fn")
class TestFloydWarshall(AllPairsShortestPaths):
    shortest_paths_fn = floyd_warshall_shortest_paths
