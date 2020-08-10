import heapq
from typing import List, Optional, Set, Tuple

from src.structures import Graph


def dijkstra(graph: Graph[str, float], start: str, end: str) -> Optional[float]:
    """
    Return the cost of the shortest path between vertices start and end.
    Cost is first in the tuple because heaps are sorted by the first element.
    """
    heap: List[Tuple[float, str]] = [(0, start)]
    visited: Set[str] = set()
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
