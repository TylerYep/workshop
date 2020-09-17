import random
from typing import Set, Tuple

from src.structures import Graph


def kargers(graph: Graph[str]) -> Set[Tuple[str, str]]:
    """
    Partitions a graph using Karger's Algorithm. Implemented from
    pseudocode found here:
    https://en.wikipedia.org/wiki/Karger%27s_algorithm.
    This function involves random choices, meaning it will not give
    consistent outputs.
    Args:
        graph: A dictionary containing adacency lists for the graph.
            Nodes must be strings.
    Returns:
        The cutset of the cut found by Karger's Algorithm.
    >>> graph = {'0':['1'], '1':['0']}
    >>> partition_graph(graph)
    {('0', '1')}
    """
    # Dict that maps contracted nodes to a set of all the nodes it "contains."
    contracted_nodes = {node: {node} for node in graph}

    graph_copy = {node: list(graph[node]) for node in graph}

    while len(graph_copy) > 2:

        # Choose a random edge.
        u = random.choice(list(graph_copy.keys()))
        v = random.choice(graph_copy[u])

        # Contract edge (u, v) to new node uv
        uv = u + v

        # Use sorted here to make this deterministic TODO change this
        uv_neighbors = sorted(set(graph_copy[u] + graph_copy[v]))
        uv_neighbors.remove(u)
        uv_neighbors.remove(v)
        graph_copy[uv] = uv_neighbors
        for neighbor in uv_neighbors:
            graph_copy[neighbor].append(uv)

        contracted_nodes[uv] = set(contracted_nodes[u].union(contracted_nodes[v]))

        # Remove nodes u and v.
        del graph_copy[u]
        del graph_copy[v]
        for neighbor in uv_neighbors:
            if u in graph_copy[neighbor]:
                graph_copy[neighbor].remove(u)
            if v in graph_copy[neighbor]:
                graph_copy[neighbor].remove(v)

    # Find cutset.
    groups = [contracted_nodes[node] for node in graph_copy]
    return {
        (node, neighbor)
        for node in groups[0]
        for neighbor in graph[node]
        if neighbor in groups[1]
    }
