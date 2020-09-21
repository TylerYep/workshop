from src.algorithms import floyd_warshall
from src.structures import Graph


def test_floyd_warshall() -> None:
    INF = Graph.INFINITY
    graph = Graph.from_matrix(
        [[0, 5, INF, 10], [INF, 0, 3, INF], [INF, INF, 0, 1], [INF, INF, INF, 0]]
    ).to_matrix()

    assert floyd_warshall(graph) == [
        [0, 5, 8, 9],
        [INF, 0, 3, 4],
        [INF, INF, 0, 1],
        [INF, INF, INF, 0],
    ]
