from typing import Union

import pytest

from src.structures import Edge, Graph, Node


def test_custom_node_edge_graph() -> None:
    graph = Graph[Node[int]]()
    nodes = [Node(i) for i in range(5)]
    for i in range(5):
        graph.add_node(nodes[i])

    graph.add_edge(nodes[0], nodes[1], 15, custom_attr="hello")
    for i in range(3, 5):
        for j in range(1, 4):
            graph.add_edge(nodes[i], nodes[j], i + j, custom_attr=str(j - i))

    assert len(graph) == 5
    assert list(graph.nodes) == nodes
    assert len(graph.edges) == 7
    for i, node in enumerate(graph):
        assert node == Node(i)
        for neighbor in graph[node]:
            assert graph[node][neighbor]["custom_attr"] is not None

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
    graph = Graph[str]()
    for item in vertices:
        graph.add_node(item)

    graph.add_edge("hi", "hello", 3)
    for str_1 in vertices[3:]:
        for str_2 in vertices[1:4]:
            graph.add_edge(str_1, str_2, abs(len(str_1) - len(str_2)))

    assert len(graph) == 4
    assert len(graph.nodes) == 4
    assert len(graph.edges) == 4
    assert graph.edges == {
        Edge("hi", "hello", 3),
        Edge("bye", "hello", 2),
        Edge("bye", "what up", 4),
        Edge("bye", "bye", 0),
    }
    assert list(graph.adj("bye")) == ["hello", "what up", "bye"]
    assert graph.degree("bye") == 3

    for i, node in enumerate(graph):
        assert node == vertices[i]


def test_bipartite() -> None:
    graph: Graph[int] = Graph.from_iterable(
        {0: [1, 3], 1: [0, 2], 2: [1, 3], 3: [0, 2], 4: []}
    )
    assert graph.is_bipartite()


def test_to_matrix() -> None:
    INF = Graph.INFINITY
    matrix = [
        [INF, 1, 5, INF],
        [1, INF, 8, INF],
        [5, 8, INF, 8],
        [INF, INF, 8, 1],
    ]
    assert Graph.from_matrix(matrix).to_matrix() == matrix

    matrix = [
        [INF, 1, 5, INF],
        [INF, INF, 2, INF],
        [INF, INF, INF, 8],
        [INF, INF, INF, 1],
    ]
    assert Graph.from_matrix(matrix).to_matrix() == matrix

    graph = Graph[int]()
    graph.add_node(3)
    graph.add_node(2)
    graph.add_node(1)
    graph.add_node(5)
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(3, 5)
    new_matrix = graph.to_matrix()

    assert new_matrix == [
        [INF, 1, 1, INF],
        [INF, INF, INF, INF],
        [INF, INF, INF, 1],
        [INF, INF, INF, INF],
    ]


def test_from_graph() -> None:
    graph = Graph[Node[int]]()
    nodes = [Node(i) for i in range(5)]
    for node in nodes:
        graph.add_node(node)
    graph.add_edge(nodes[0], nodes[1], 15)
    for i in range(3, 5):
        for j in range(1, 4):
            graph.add_edge(nodes[i], nodes[j], i + j)

    new_graph = Graph.from_graph(graph)
    assert graph == new_graph

    for i in range(3):
        graph.remove_node(nodes[i])
    assert len(graph) == 2
    assert len(graph.edges) == 2

    # Verify that we have not modified the original graph
    assert len(graph) != len(new_graph)
    assert len(graph.edges) != len(new_graph)
    assert graph != new_graph


def test_comparable_types() -> None:
    graph = Graph[int]()
    for i in range(5):
        graph.add_node(i)

    graph.add_edge(2, 2)
    graph.add_edge(1, 3)
    assert sorted(graph.nodes) == list(range(5))
    assert sorted(graph.edges) == [Edge(1, 3), Edge(2, 2)]


def test_noncomparable_types() -> None:
    graph = Graph[Union[str, int]]()
    for i in range(5):
        graph.add_node(i)
        graph.add_node(str(i))

    with pytest.raises(TypeError):
        _ = sorted(graph)


def test_print_graph() -> None:
    graph = Graph[int]()
    for i in range(4):
        graph.add_node(i)

    graph.add_edge(0, 1)
    for i in range(2):
        for j in range(1, 4):
            graph.add_edge(i, j)

    graph_str = str(graph)
    assert graph_str == (
        "{\n"
        "    0: {\n"
        "        1: Edge(start=0, end=1, weight=1),\n"
        "        2: Edge(start=0, end=2, weight=1),\n"
        "        3: Edge(start=0, end=3, weight=1)\n"
        "    },\n"
        "    1: {\n"
        "        1: Edge(start=1, end=1, weight=1),\n"
        "        2: Edge(start=1, end=2, weight=1),\n"
        "        3: Edge(start=1, end=3, weight=1)\n"
        "    },\n"
        "    2: {},\n"
        "    3: {}\n"
        "}"
    )
    graph_str = (
        graph_str.replace("\n", "")
        .replace(" " * 4, "")
        .replace("},", "}, ")
        .replace("),", "), ")
    )
    assert repr(graph) == (f"Graph(_graph={graph_str}, is_directed=True)")
