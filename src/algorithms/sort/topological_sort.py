from typing import Any, List, Set, TypeVar

from src.structures import Graph

V = TypeVar("V")


def topological_sort(graph: Graph[V, Any], start: V) -> List[V]:
    def _topological_sort(current: V, visited: Set[V], sort: List[V]) -> List[V]:
        """Perform topolical sort on a directed acyclic graph."""
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                sort = _topological_sort(neighbor, visited, sort)
        # if all neighbors visited add current to sort
        sort.append(current)
        # if all vertices haven't been visited select a new one to visit
        if len(visited) != len(graph):
            for vertice in graph:
                if vertice not in visited:
                    sort = _topological_sort(vertice, visited, sort)
        return sort

    return _topological_sort(start, set(), [])
