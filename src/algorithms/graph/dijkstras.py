import heapq
from typing import Dict, List, Optional, Set, Tuple

from src.structures import FibonacciHeap, Graph, V


def dijkstra_search(graph: Graph[V], start: V, end: V) -> Optional[float]:
    """
    Identical to BFS and DFS, except uses a priority queue and weights from the graph.

    Returns the cost of the shortest path between vertices start and end.
    Cost is first in the tuple because heaps are sorted by the first element.

    Runtime: O(|E| + |V| log |V|)
    """
    heap = FibonacciHeap[V]()
    heap.enqueue(start, 0)
    for node in graph:
        if node != start:
            heap.enqueue(node, Graph.INFINITY)
    distances = {}
    while heap:
        # The algorithm guarantees that we now have the shortest distance to u.
        u, cost = heap.dequeue_min()
        if u == end:
            return cost
        distances[u] = cost
        for v, e in graph[u].items():
            if v not in distances:
                path_cost = cost + e.weight
                if path_cost < heap[v].priority:
                    heap.decrease_key(v, path_cost)
    return None


def dijkstra_shortest_distances(graph: Graph[V], start: V) -> Dict[V, float]:
    """
    Given a directed, weighted graph G and a source node s, produces the
    distances from s to each other node in the graph.  If any nodes in
    the graph are unreachable from s, they will be reported at distance +infinity.
    Runtime: O(|E| + |V| log |V|)
    """
    heap = FibonacciHeap[V]()
    heap.enqueue(start, 0)
    for node in graph:
        if node != start:
            heap.enqueue(node, Graph.INFINITY)
    distances = {}
    while heap:
        # The algorithm guarantees that we now have the shortest distance to u.
        u, cost = heap.dequeue_min()
        distances[u] = cost
        for v, e in graph[u].items():
            if v not in distances:
                path_cost = cost + e.weight
                if path_cost < heap[v].priority:
                    heap.decrease_key(v, path_cost)
    return distances


def dijkstra_search_heapq(graph: Graph[V], start: V, end: V) -> Optional[float]:
    """
    Identical to BFS and DFS, except uses a priority queue and weights from the graph.

    Returns the cost of the shortest path between vertices start and end.
    Cost is first in the tuple because heaps are sorted by the first element.

    Runtime: O(|E + V| log |V|)
    """
    heap: List[Tuple[float, V]] = [(0, start)]
    visited: Set[V] = set()
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


def dijkstra_shortest_distances_heapq(graph: Graph[V], start: V) -> Dict[V, float]:
    heap: List[Tuple[float, V]] = [(0.0, start)]
    visited: Set[V] = set()
    distances = {node: Graph.INFINITY for node in graph}
    distances[start] = 0.0
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
