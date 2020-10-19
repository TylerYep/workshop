from src.algorithms import prims_mst
from src.structures import Graph


def test_prims() -> None:
    INF = Graph.INFINITY
    g = Graph.from_matrix(
        [
            [INF, 2, INF, 6, INF],
            [2, INF, 3, 8, 5],
            [INF, 3, INF, INF, 7],
            [6, 8, INF, INF, 9],
            [INF, 5, 7, 9, INF],
        ]
    )

    assert prims_mst(g) == Graph(
        {
            0: {1: 2, 3: 6},
            1: {
                0: 2,
                2: 3,
                4: 5,
            },
            2: {1: 3},
            4: {1: 5},
            3: {0: 6},
        },
        is_directed=False,
    )
