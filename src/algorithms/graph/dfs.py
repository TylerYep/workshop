from typing import List, Optional, Set, Tuple, TypeVar

from src.structures import Graph

V = TypeVar("V")


def depth_first_search(graph: Graph[V], start: V, end: V) -> Optional[List[V]]:
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


def depth_first_search_recursive(
    graph: Graph[V], start: V, end: V
) -> Optional[List[V]]:
    """
    Recursive version of DFS.

    Runtime: O(V + E)
    """

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


def dfs_traversal(graph: Graph[V], start: V, visited: Optional[Set[V]]) -> Set[V]:
    """
    Explores graph starting with start using a depth-first-search traversal.
    Modifies a visited set in place, and returns a set of connected vertices.

    Runtime: O(V + E)
    """
    if visited is None:
        visited = set()
    visited.add(start)
    connected_nodes = {start}
    for neighbor in graph[start]:
        if neighbor not in visited:
            connected_nodes |= dfs_traversal(graph, neighbor, visited)
    return connected_nodes
