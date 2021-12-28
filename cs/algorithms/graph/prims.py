from __future__ import annotations

from cs.structures import FibonacciHeap, Graph, V


def prims_mst(graph: Graph[V], start_node: V | None = None) -> Graph[V]:
    """
    Given a connected, undirected graph with real-valued edge costs, returns an MST of
    that graph.

    The key difference between Dijkstra's algorithm and Prim's algorithm is that
    Dijkstra's algorithm creates a shortest-path tree from the source node, while Prim's
    algorithm builds an MST from the source node.

    First, we do O(|V|) insertions into the heap. We then do O(|V|) dequeues (since we
    only want a total of |V| - 1 edges). These dequeues take a total of O(|V| log |V)
    time, though any one dequeue might take much more than that. Finally, on each
    dequeue, we scan all outgoing edges from the dequeued node. Since we never consider
    a node twice, the total number of edges visited must be twice the number of edges in
    the graph, since each edge will be visited once from each endpoint, which is O(|E|)
    addiional time.

    Runtime: O(|E| + |V| log |V|)
    """
    mst = Graph[V](is_directed=False)
    if not graph:
        return mst

    heap = FibonacciHeap[V]()
    start = start_node or next(iter(graph))
    mst.add_node(start)
    _add_outgoing_edges(graph, start, mst, heap)

    for _ in range(len(graph) - 1):
        # The algorithm guarantees that we now have the shortest distance to u.
        u, _ = heap.dequeue()
        v, weight = _min_cost_endpoint(u, graph, mst)
        mst.add_node(u)
        mst.add_edge(u, v, weight)
        _add_outgoing_edges(graph, u, mst, heap)
    return mst


def _add_outgoing_edges(
    graph: Graph[V], u: V, mst: Graph[V], heap: FibonacciHeap[V]
) -> None:
    """
    Given a node, updates the priorities of adjacent nodes by following its edges.
    """
    for v, e in graph[u].items():
        if v in mst:
            continue
        if v not in heap:
            heap.enqueue(v, e.weight)
        elif heap[v].priority > e.weight:
            heap.decrease_key(v, e.weight)


def _min_cost_endpoint(node: V, graph: Graph[V], mst: Graph[V]) -> tuple[V, float]:
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
        raise AssertionError("Since we dequeued this node, it has at least 1 neighbor.")
    return end, least_cost
