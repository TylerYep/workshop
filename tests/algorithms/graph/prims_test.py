from src.algorithms import prims_mst
from src.structures import Graph


def test_prims() -> None:
    g = Graph.from_matrix(
        [
            [0, 2, 0, 6, 0],
            [2, 0, 3, 8, 5],
            [0, 3, 0, 0, 7],
            [6, 8, 0, 0, 9],
            [0, 5, 7, 9, 0],
        ],
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
