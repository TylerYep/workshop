import random
from typing import Set, Tuple, TypeVar

from src.structures import Edge, Graph, Node

V = TypeVar("V")


def kargers(orig_graph: Graph[V]) -> Set[Edge[V]]:
    """
    Partitions a graph using Karger's Algorithm.
    Works on directed and undirected graphs.
    This function involves random choices, so it does not give consistent outputs.
    Args:
        graph: A dictionary containing adacency lists for the graph.
            Nodes must be strings.
    Returns:
        The cutset of the cut found by Karger's Algorithm.
    >>> graph = {'0':['1'], '1':['0']}
    >>> partition_graph(graph)
    {('0', '1')}
    """
    graph: Graph[Node[Tuple[V, ...]]] = Graph.from_graph(
        orig_graph, node_fn=lambda x: Node((x,))
    )

    while len(graph) > 2:
        edge = random.choice(graph.edges)

        # Contract edge (u, v) to new node uv
        uv = Node(edge.start.data + edge.end.data)

        # TODO Python 3.9 - graph[edge.start] | graph[edge.end]
        uv_neighbors = {**graph[edge.start], **graph[edge.end]}
        del uv_neighbors[edge.start]
        del uv_neighbors[edge.end]

        graph.add_node(uv)
        for neighbor in uv_neighbors:
            graph.add_edge(uv, neighbor)
            graph.add_edge(neighbor, uv)

        # Remove nodes u and v.
        graph.remove_node(edge.start)
        graph.remove_node(edge.end)

    # Find cutset.
    group1, group2 = graph.nodes
    result_set = set()
    for subnode in group1.data:
        for subneighbor in group2.data:
            if subneighbor in orig_graph[subnode] or subnode in orig_graph[subneighbor]:
                result_set.add(orig_graph[subnode][subneighbor])

    return result_set