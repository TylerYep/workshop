from __future__ import annotations

import heapq

from cs.structures import FibonacciHeap, Graph, V


def dijkstra_search(graph: Graph[V], start: V, end: V) -> float | None:
    """
    Identical to BFS and DFS, except uses a priority queue and weights from the graph.

    Returns the cost of the shortest path between vertices start and end.
    Cost is first in the tuple because heaps are sorted by the first element.

    Runtime: O(|E| + |V| log |V|)
    """
    heap = FibonacciHeap[V]()
    heap.enqueue(start, 0)
    for v in graph:
        if v != start:
            heap.enqueue(v, Graph.INFINITY)
    distances = {}
    while heap:
        # The algorithm guarantees that we now have the shortest distance to u.
        u, cost = heap.dequeue()
        if u == end:
            return cost
        distances[u] = cost
        for v, e in graph[u].items():
            if v not in distances:
                path_cost = cost + e.weight
                if path_cost < heap[v].priority:
                    heap.decrease_key(v, path_cost)
    return None


def dijkstra_shortest_paths(graph: Graph[V], start: V) -> dict[V, float]:
    """
    Dijkstra's algorithm for the single-source shortest paths problem.

    Given a directed, weighted graph G and a source node s, produces the distances from
    s to each other node in the graph. If any nodes in the graph are unreachable from s,
    they will be reported at distance +infinity.

    The code makes up to |E| calls to decrease-key on the heap (worst case, every edge
    from every node yields a shorter path than before) and |V| calls to dequeue-min
    (each node is removed from the heap at most once).

    Runtime: O(|E| + |V| log |V|)
    """
    heap = FibonacciHeap[V]()
    heap.enqueue(start, 0)
    for v in graph:
        if v != start:
            heap.enqueue(v, Graph.INFINITY)
    distances = {}
    while heap:
        # The algorithm guarantees that we now have the shortest distance to u.
        u, cost = heap.dequeue()
        distances[u] = cost
        for v, e in graph[u].items():
            if v not in distances:
                if e.weight < 0:
                    raise RuntimeError("Dijkstra's does not work for negative weights.")
                path_cost = cost + e.weight
                if path_cost < heap[v].priority:
                    heap.decrease_key(v, path_cost)
    return distances


def dijkstra_search_heapq(graph: Graph[V], start: V, end: V) -> float | None:
    """
    Identical to BFS and DFS, except uses a priority queue and weights from the graph.

    Returns the cost of the shortest path between vertices start and end.
    Cost is first in the tuple because heaps are sorted by the first element.

    Runtime: O(|E + V| log |V|)
    """
    heap: list[tuple[float, V]] = [(0, start)]
    visited: set[V] = set()
    while heap:
        cost, u = heapq.heappop(heap)
        if u == end:
            return cost
        if u not in visited:
            visited.add(u)
            for v, e in graph[u].items():
                if v not in visited:
                    heapq.heappush(heap, (cost + e.weight, v))
    return None


def dijkstra_shortest_paths_heapq(graph: Graph[V], start: V) -> dict[V, float]:
    heap: list[tuple[float, V]] = [(0, start)]
    visited: set[V] = set()
    distances = {v: Graph.INFINITY for v in graph}
    distances[start] = 0
    while heap:
        cost, u = heapq.heappop(heap)
        if u not in visited:
            visited.add(u)
            for v, e in graph[u].items():
                if distances[u] + cost < distances[v]:
                    distances[v] = distances[u] + e.weight
                    if v not in visited:
                        heapq.heappush(heap, (cost + e.weight, v))
    return distances
