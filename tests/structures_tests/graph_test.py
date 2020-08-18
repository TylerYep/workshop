import pytest

from src.structures import Edge, Graph, Node


def test_custom_node_edge_graph() -> None:
    graph = Graph[Node[int], Edge[int]]()
    nodes = [Node(i) for i in range(5)]
    for i in range(5):
        graph.add_node(nodes[i])

    graph.add_edge(nodes[0], nodes[1], Edge(0, 1, weight=15))
    for i in range(3, 5):
        for j in range(1, 4):
            graph.add_edge(nodes[i], nodes[j], Edge(i, j, weight=i + j))

    assert len(graph) == 5
    assert list(graph.nodes) == nodes
    assert len(graph.edges) == 7
    for i, node in enumerate(graph):
        assert node == Node(i)

    node_3 = nodes[3]
    assert list(graph.adj(node_3)) == nodes[1:4]
    assert graph.degree(node_3) == 4
    assert graph.out_degree(node_3) == 3
    assert graph.in_degree(node_3) == 1
    assert not graph.is_bipartite()

    with pytest.raises(KeyError):
        graph.remove_node(Node(7))

    for i in range(3):
        graph.remove_node(nodes[i])
    assert len(graph) == 2
    assert len(graph.edges) == 2


def test_int_directed_graph() -> None:
    graph = Graph[int, None]()
    for i in range(5):
        graph.add_node(i)

    graph.add_edge(0, 1)
    for i in range(3, 5):
        for j in range(1, 4):
            graph.add_edge(i, j)

    assert len(graph) == 5
    assert list(graph.nodes) == list(range(5))
    assert len(graph.edges) == 7
    for i, node in enumerate(graph):
        assert node == i

    assert list(graph.adj(3)) == [1, 2, 3]
    assert graph.degree(3) == 4
    assert graph.out_degree(3) == 3
    assert graph.in_degree(3) == 1
    assert not graph.is_bipartite()

    with pytest.raises(KeyError):
        graph.remove_node(7)

    for i in range(3):
        graph.remove_node(i)
    assert len(graph) == 2
    assert len(graph.edges) == 2


def test_int_undirected_graph() -> None:
    graph = Graph[int, None](is_directed=False)
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
    assert not graph.is_bipartite()
    for i, node in enumerate(graph):
        assert node == i

    with pytest.raises(KeyError):
        graph.remove_node(7)

    for i in range(3):
        graph.remove_node(i)
    assert len(graph) == 2
    assert len(graph.edges) == 3


def test_str_adj_graph() -> None:
    vertices = ["hi", "hello", "what up", "bye"]
    graph = Graph[str, float]()
    for item in vertices:
        graph.add_node(item)

    graph.add_edge("hi", "hello", 3)
    for str_1 in vertices[3:]:
        for str_2 in vertices[1:4]:
            graph.add_edge(str_1, str_2, abs(len(str_1) - len(str_2)))

    assert len(graph) == 4
    assert len(graph.nodes) == 4
    assert len(graph.edges) == 4
    assert graph.edges == [3, 2, 4, 0]
    assert list(graph.adj("bye")) == ["hello", "what up", "bye"]
    assert graph.degree("bye") == 3

    for i, node in enumerate(graph):
        assert node == vertices[i]


def test_bipartite() -> None:
    graph: Graph[int, None] = Graph.from_iterable(
        {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: []}
    )
    assert graph.is_bipartite()
