import heapq
from typing import Any, Optional


def dijkstra(graph: Any, start: str, end: str) -> Optional[float]:
    """
    Return the cost of the shortest path between vertices start and end.
    """
    heap = [(0, start)]
    visited = set()
    while heap:
        (cost, u) = heapq.heappop(heap)
        if u == end:
            return cost

        if u not in visited:
            visited.add(u)
            for v, c in graph[u].items():
                if v not in visited:
                    next_cost = cost + c
                    heapq.heappush(heap, (next_cost, v))
    return None
