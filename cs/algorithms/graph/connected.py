from typing import Set

from cs.structures import Graph, V


def connected_components(graph: Graph[V]) -> list[Set[V]]:
    """
    This function returns the list of connected components of the given Graph.

    Runtime: O(V + E)
    """
    from cs.algorithms import dfs_traversal

    visited: Set[V] = set()
    components_list: list[Set[V]] = []
    for v in graph:
        if v not in visited:
            components_list.append(dfs_traversal(graph, v, visited))
    return components_list
