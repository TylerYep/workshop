from collections import deque
from typing import Deque, List, Optional, Set, Tuple

from src.structures import Graph, V


def breadth_first_search(graph: Graph[V], start: V, end: V) -> Optional[List[V]]:
    """
    Identical to DFS except with a queue and pop(0).
    Does not benefit from an additional visited check because it uses a queue.

    Runtime: O(V + E)
    """
    queue: Deque[Tuple[V, List[V]]] = deque([(start, [start])])
    visited: Set[V] = set()
    while queue:
        vertex, path = queue.popleft()
        if vertex == end:
            return path
        visited.add(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    return None
