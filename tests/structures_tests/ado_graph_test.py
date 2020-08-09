import random

from src.structures.ado import ApproxDistanceOracle

INF = 1000


def test_zero_distance_approx() -> None:
    random.seed(0)

    vertices = set(range(4))
    # INF means there is no edge between the vertices
    edges = [
        [0, 4, 3, INF],
        [4, 0, 2, INF],
        [3, 2, 0, 1],
        [INF, INF, 1, 0],
    ]

    ado = ApproxDistanceOracle(vertices, edges)
    # The true min distance is 4, but the oracle's estimate is 5
    assert ado.query(0, 1) == 5
