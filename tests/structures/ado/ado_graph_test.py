from cs.structures import ApproxDistanceOracle, Graph


def test_zero_distance_approx() -> None:
    INF = Graph.INFINITY
    # INF means there is no edge between the vertices
    graph = Graph.from_matrix(
        [
            [0, 4, 3, INF],
            [4, 0, 2, INF],
            [3, 2, 0, 1],
            [INF, INF, 1, 0],
        ],
        zero_is_no_edge=False,
    )

    ado = ApproxDistanceOracle(graph)
    # The true min distance is 4, but the oracle's estimate is 5
    assert ado.query(0, 1) == 5
