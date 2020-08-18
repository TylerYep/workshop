from typing import Any, List, Set, TypeVar

from src.structures import Graph

V = TypeVar("V")


def connected_components(graph: Graph[V, Any]) -> List[Set[V]]:
    """
    This function returns the list of connected components of the given Graph.
    """
    from src.algorithms import dfs_traversal

    visited: Set[V] = set()
    components_list: List[Set[V]] = []
    for node in graph:
        if node not in visited:
            components_list.append(dfs_traversal(graph, node, visited))
    return components_list
