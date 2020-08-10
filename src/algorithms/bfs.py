from typing import Any, List, Optional, Set, Tuple, TypeVar

from src.structures import Graph

V = TypeVar("V")


def breadth_first_search(graph: Graph[V, Any], start: V, end: V) -> Optional[List[V]]:
    """
    Identical to DFS except with a queue and pop(0).

    Runtime: O(V + E)
    """
    queue: List[Tuple[V, List[V]]] = [(start, [start])]
    visited: Set[V] = set()
    while queue:
        vertex, path = queue.pop(0)
        if vertex == end:
            return path
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None
