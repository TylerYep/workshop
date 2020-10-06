from src.algorithms import kruskals
from src.structures import Edge, Graph


def test_kruskals_small() -> None:
    graph = Graph[int]()
    for i in range(4):
        graph.add_node(i)
    graph.add_edge(0, 1, 10)
    graph.add_edge(0, 2, 6)
    graph.add_edge(0, 3, 5)
    graph.add_edge(1, 3, 15)
    graph.add_edge(2, 3, 4)

    assert kruskals(graph) == {
        Edge(2, 3, 4),
        Edge(0, 3, 5),
        Edge(0, 1, 10),
    }


def test_kruskals() -> None:
    graph = Graph[int]()
    for i in range(6):
        graph.add_node(i)
    graph.add_edge(0, 1, 4)
    graph.add_edge(0, 2, 4)
    graph.add_edge(1, 2, 2)
    graph.add_edge(1, 0, 4)
    graph.add_edge(2, 0, 4)
    graph.add_edge(2, 1, 2)
    graph.add_edge(2, 3, 3)
    graph.add_edge(2, 5, 2)
    graph.add_edge(2, 4, 4)
    graph.add_edge(3, 2, 3)
    graph.add_edge(3, 4, 3)
    graph.add_edge(4, 2, 4)
    graph.add_edge(4, 3, 3)
    graph.add_edge(5, 2, 1)
    graph.add_edge(5, 4, 3)

    assert kruskals(graph) == {
        Edge(5, 2, 1),
        Edge(3, 2, 3),
        Edge(2, 1, 2),
        Edge(5, 4, 3),
        Edge(1, 0, 4),
    }