from cs.structures import Graph, V


def connected_components(graph: Graph[V]) -> list[set[V]]:
    """
    This function returns the list of connected components of the given Graph.

    Runtime: O(V + E)
    """
    from cs.algorithms import dfs_traversal

    visited: set[V] = set()
    components_list: list[set[V]] = [
        dfs_traversal(graph, v, visited) for v in graph if v not in visited
    ]
    return components_list
