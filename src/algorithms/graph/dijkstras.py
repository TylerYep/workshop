import heapq
from typing import Dict, List, Optional, Set, Tuple, TypeVar

from src.structures import Graph

V = TypeVar("V")


def dijkstra_search(graph: Graph[V, float], start: V, end: V) -> Optional[float]:
    """
    Identical to BFS and DFS, except uses a priority queue and gets weights from the graph.

    Returns the cost of the shortest path between vertices start and end.
    Cost is first in the tuple because heaps are sorted by the first element.

    Runtime: O(V + E)
    """
    heap: List[Tuple[float, V]] = [(0, start)]
    visited: Set[V] = set()
    while heap:
        cost, u = heapq.heappop(heap)
        if u == end:
            return cost
        if u not in visited:
            visited.add(u)
            for v, c in graph[u].items():
                if v not in visited:
                    heapq.heappush(heap, (cost + c, v))
    return None


def dijkstra_shortest_distances(graph: Graph[V, float], start: V) -> Dict[V, float]:
    distances = {start: 0.0}
    visited: Set[V] = set()
    path = {start: start}
    INF = float("inf")
    while len(visited) != len(graph) - 1:
        mini = INF
        for i in distances:
            if i not in visited and distances[i] < mini:
                mini = distances[i]
                u = i
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                if distances[u] + graph[u][v] < distances.get(v, INF):
                    distances[v] = distances[u] + graph[u][v]
                    path[v] = u
    return distances
