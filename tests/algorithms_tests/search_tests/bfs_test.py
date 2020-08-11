from src.algorithms import breadth_first_search
from src.structures import Graph


def test_bfs() -> None:
    graph: Graph[str, None] = Graph.from_iterable(
        {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"],
        }
    )
    assert breadth_first_search(graph, "A", "F") == ["A", "C", "F"]

    graph_2: Graph[int, None] = Graph.from_iterable(
        {0: [1, 2], 1: [0, 3, 4], 2: [0, 3], 3: [1], 4: [2, 3]}
    )

    assert breadth_first_search(graph_2, 0, 4) == [0, 1, 4]
