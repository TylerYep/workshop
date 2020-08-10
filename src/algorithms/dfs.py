from typing import List, Optional, Set, Tuple

from src.structures import Graph


def depth_first_search(graph: Graph[str, str], start: str, end: str) -> Optional[List[str]]:
    """ Iterative version of DFS. """
    stack: List[Tuple[str, List[str]]] = [(start, [start])]
    visited: Set[str] = set()
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
    graph: Graph[str, str], start: str, end: str
) -> Optional[List[str]]:
    """ Recursive version of DFS. """

    def _dfs(curr: str, visited: Set[str], path: List[str]) -> Optional[List[str]]:
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
