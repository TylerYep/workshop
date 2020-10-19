from typing import Dict

from src.structures import Graph, V


def bellman_ford(
    graph: Graph[V], start: V, *, check_negative_cycles: bool = True
) -> Dict[V, float]:
    """
    The Bellman-Ford algorithm computes the shortest paths from a source node to
    all other nodes in the graph, like Dijkstr'as algorithm, however with the added
    guarantee that the Bellman-Ford algorithm works correctly in graphs containing
    negative-cost edges, so long as the graph does not contain a negative cycle
    (in which case the cost of a shortest path may not be well-defined).

    If |E| = O(|V|^2), then running the Floyd-Warshall algorithm makes more sense,
    to get all shortest path pairs rather than just one. However, on sparse graphs
    where |E| = Theta(|V|)) the runtime is O(|V|^2), which is much faster.

    Runtime: O(|V||E|), or worst case, O(|V|^3).
    """
    distances = {v: Graph.INFINITY for v in graph}
    distances[start] = 0.0

    for _ in range(1, len(graph)):
        temp = distances
        for u in graph:
            for v, e in graph[u].items():
                temp[v] = min(temp[v], distances[u] + e.weight)

        distances, temp = temp, distances

    if check_negative_cycles:
        for edge in graph.edges:
            if distances[edge.end] > distances[edge.start] + edge.weight:
                raise AssertionError("Negative weight cycle exists in the graph.")

    return distances
