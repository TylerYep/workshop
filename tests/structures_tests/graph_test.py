import pytest

from src.structures.graph import Graph


def test_int_directed_graph() -> None:
    graph = Graph[int]()
    for i in range(5):
        graph.add_node(i)

    graph.add_edge(0, 1)
    for i in range(3, 5):
        for j in range(1, 4):
            graph.add_edge(i, j)

    assert len(graph) == 5
    assert list(graph.nodes) == list(range(5))
    assert len(graph.edges) == 7
    assert list(graph.adj(3)) == [1, 2, 3]
    assert graph.degree(3) == 3
    for i, node in enumerate(graph):
        assert node == i

    with pytest.raises(KeyError):
        graph.remove_node(7)

    for i in range(3):
        graph.remove_node(i)
    graph.remove_edge(3, 1)
    assert len(graph) == 2
    assert len(graph.edges) == 2


def test_int_undirected_graph() -> None:
    graph = Graph[int](is_directed=False)
    for i in range(5):
        graph.add_node(i)

    graph.add_edge(0, 1)
    for i in range(3, 5):
        for j in range(1, 4):
            graph.add_edge(i, j)

    assert len(graph) == 5
    assert list(graph.nodes) == list(range(5))
    assert len(graph.edges) == 13
    assert list(graph.adj(3)) == [1, 2, 3, 4]
    assert graph.degree(3) == 4
    for i, node in enumerate(graph):
        assert node == i

    with pytest.raises(KeyError):
        graph.remove_node(7)

    for i in range(3):
        graph.remove_node(i)
    graph.remove_edge(3, 1)
    assert len(graph) == 2
    assert len(graph.edges) == 3


def test_str_adj_graph() -> None:
    vertices = ["hi", "hello", "what up", "bye"]
    graph = Graph[str]()
    for item in vertices:
        graph.add_node(item)

    graph.add_edge("hi", "hello")
    for str_1 in vertices[3:]:
        for str_2 in vertices[1:4]:
            graph.add_edge(str_1, str_2)

    assert len(graph) == 4
    assert len(graph.nodes) == 4
    assert len(graph.edges) == 4
    assert list(graph.adj("bye")) == ["hello", "what up", "bye"]
    assert graph.degree("bye") == 3

    for i, node in enumerate(graph):
        assert node == vertices[i]
