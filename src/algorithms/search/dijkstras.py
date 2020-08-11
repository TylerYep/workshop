import heapq
from typing import List, Optional, Set, Tuple, TypeVar

from src.structures import Graph

V = TypeVar("V")


def dijkstra_search(graph: Graph[V, float], start: V, end: V) -> Optional[float]:
    """
    Identical to BFS and DFS, except uses a priority queue and gets weights from the graph.

    Returns the cost of the shortest path between vertices start and end.
    Cost is first in the tuple because heaps are sorted by the first element.
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
