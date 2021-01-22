from cs.structures import Graph, V


def topological_sort(graph: Graph[V]) -> list[V]:
    """
    Perform topological sort on a directed acyclic graph.

    Node never seen = not in visited
    Node being processed = in visited but not in stack
    Node done = in stack

    Runtime: O(V + E)
    """

    def depth_first_search(v: V, visited: set[V], stack: list[V]) -> None:
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor in visited and neighbor not in stack:
                raise ValueError(f"Cycle detected in node {v}")
            if neighbor not in visited:
                depth_first_search(neighbor, visited, stack)
        stack.append(v)

    stack: list[V] = []
    visited: set[V] = set()
    for v in graph:
        if len(visited) == len(graph):
            break
        if v not in visited:
            depth_first_search(v, visited, stack)
    return stack
