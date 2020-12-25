from src.algorithms import ford_max_flow
from src.structures import Graph


def test_ford() -> None:
    graph = Graph.from_matrix(
        [
            [0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ],
    )

    result = ford_max_flow(graph, 0, 5)

    assert sum(edge["flow"] for edge in result[0].values()) == 23


def test_ford_brilliant() -> None:
    graph = Graph[str]()
    for letter in ("s", "t", "a", "b", "c", "d"):
        graph.add_node(letter)
    graph.add_edge("s", "a", 4)
    graph.add_edge("a", "b", 4)
    graph.add_edge("b", "t", 2)
    graph.add_edge("s", "c", 3)
    graph.add_edge("c", "d", 6)
    graph.add_edge("d", "t", 6)
    graph.add_edge("b", "c", 3)

    result = ford_max_flow(graph, "s", "t")

    assert sum(edge["flow"] for edge in result["s"].values()) == 7
