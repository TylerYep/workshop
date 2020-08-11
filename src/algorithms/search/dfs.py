from typing import Any, List, Optional, Set, Tuple, TypeVar

from src.structures import Graph

V = TypeVar("V")


def depth_first_search(graph: Graph[V, Any], start: V, end: V) -> Optional[List[V]]:
    """
    Iterative version of DFS.

    Runtime: O(V + E)
    """
    stack: List[Tuple[V, List[V]]] = [(start, [start])]
    visited: Set[V] = set()
    while stack:
        vertex, path = stack.pop()
        if vertex == end:
            return path
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None


def depth_first_search_recursive(graph: Graph[V, Any], start: V, end: V) -> Optional[List[V]]:
    """ Recursive version of DFS. """

    def _dfs(curr: V, visited: Set[V], path: List[V]) -> Optional[List[V]]:
        if curr == end:
            return path
        if curr not in visited:
            visited.add(curr)
            for neighbor in graph[curr]:
                result = _dfs(neighbor, visited, path + [neighbor])
                if result is not None:
                    return result
        return None

    return _dfs(start, set(), [start])
