from typing import Any, List, Set, TypeVar

from src.structures import Graph

V = TypeVar("V")


def topological_sort(graph: Graph[V, Any], start: V) -> List[V]:
    def _topological_sort(current: V, visited: Set[V], result: List[V]) -> List[V]:
        """ Perform topolical sort on a directed acyclic graph. """
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                result = _topological_sort(neighbor, visited, result)
        # if all neighbors visited add current to result
        result.append(current)
        # if all vertices haven't been visited select a new one to visit
        if len(visited) != len(graph):
            for vertice in graph:
                if vertice not in visited:
                    result = _topological_sort(vertice, visited, result)
        return result

    return _topological_sort(start, set(), [])
