from typing import Optional, Tuple

from src.structures import FibonacciHeap, Graph, V


def prims(graph: Graph[V], start_node: Optional[V] = None) -> Graph[V]:
    """
    Given a connected undirected graph with real-valued edge costs,
    returns an MST of that graph.

    Runtime: O(|E| + |V| log |V|)
    """
    mst = Graph[V](is_directed=False)
    if not graph:
        return mst

    heap = FibonacciHeap[V]()
    start = next(iter(graph)) if start_node is None else start_node
    mst.add_node(start)
    _add_outgoing_edges(graph, start, mst, heap)

    for _ in range(len(graph) - 1):
        # The algorithm guarantees that we now have the shortest distance to u.
        u, _ = heap.dequeue_min()
        v, weight = _min_cost_endpoint(u, graph, mst)
        mst.add_node(v)
        mst.add_edge(u, v, weight)
        _add_outgoing_edges(graph, u, mst, heap)
    return mst


def _add_outgoing_edges(
    graph: Graph[V], u: V, mst: Graph[V], heap: FibonacciHeap[V]
) -> None:
    """
    Given a node in the graph, updates the priorities of adjacent nodes to
    take these edges into account. Due to some optimizations we make, this
    step takes in several parameters beyond what might seem initially
    required.
    """
    for v, e in graph[u].items():
        if u in mst:
            continue
        if u not in heap:
            heap.enqueue(v, e.weight)
        elif heap[u].priority > e.weight:
            heap.decrease_key(u, e.weight)


def _min_cost_endpoint(node: V, graph: Graph[V], mst: Graph[V]) -> Tuple[V, float]:
    """
    Given a node in the source graph and a set of nodes that we've visited
    so far, returns the minimum-cost edge from that node to some node that
    has been visited before.
    """
    end = None
    least_cost = Graph.INFINITY
    for neighbor, edge in graph[node].items():
        if neighbor in mst and edge.weight < least_cost:
            end = neighbor
            least_cost = edge.weight
    if end is None:
        raise AssertionError("Since we dequeued this node, it must have a neighbor.")
    return end, least_cost


# from typing import Any, Dict, Set
# from src.structures import Graph, V
# import random

# def prims(graph: Graph[V]) -> Dict[V, float]:
#     """
#     Prim's MST Algorithm
#         Args :  G - Dictionary of edges
#                 s - Starting Node
#         Vars :  distances - Dictionary storing shortest distance
#                         from s to nearest node
#                 visited - Set of visited nodes
#                 path - Preceding node in path
#     """
#     start = next(iter(graph))
#     distances = {start: 0}
#     visited: Set[V] = set()
#     path = {start: 0}
#     while len(visited) != len(graph) - 1:
#         mini = Graph.INFINITY
#         for v in distances:
#             if v not in visited and distances[v] < mini:
#                 mini = distances[v]
#                 u = v
#         visited.add(u)
#         for edge in graph[u].values():
#             if edge.start not in visited:
#                 if edge.end < distances.get(edge.start, Graph.INFINITY):
#                     distances[edge.start] = edge.end
#                     path[edge.start] = start
#     return distances
