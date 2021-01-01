from cs.algorithms import connected_components
from cs.structures import Graph


def test_connected_components() -> None:
    test_graph_1 = Graph[int](
        {0: [1, 2], 1: [0, 3], 2: [0], 3: [1], 4: [5, 6], 5: [4, 6], 6: [4, 5]}
    )
    assert connected_components(test_graph_1) == [{0, 1, 3, 2}, {4, 5, 6}]

    test_graph_2 = Graph[int](
        {0: [1, 2, 3], 1: [0, 3], 2: [0], 3: [0, 1], 4: [], 5: []}
    )
    assert connected_components(test_graph_2) == [{0, 1, 3, 2}, {4}, {5}]
