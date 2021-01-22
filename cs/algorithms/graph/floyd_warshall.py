from cs.structures import Graph, V


def floyd_warshall_shortest_paths(graph: Graph[V]) -> dict[V, dict[V, float]]:
    """
    Calculates the shortest distance between all vertex pairs using dynamic programming.
    distance[u][v] will contain the shortest distance from vertex u to v.

    1. For all edges from v to n, distance[i][j] = weight(edge(i, j)).
    3. The algorithm then performs distance[i][j] = min(distance[i][j], distance[i][k]
        + distance[k][j]) for each possible pair i, j of vertices.
    4. The above is repeated for each vertex k in the graph.
    5. Whenever distance[i][j] is given a new minimum value, next vertex[i][j] is
        updated to the next vertex[i][k].

    Unlike Dijkstra's Algorithm, the Floyd-Warshall Algorithm has no problems handling
    graphs with negative edge costs.

    Runtime: O(|V|^3) Memory: O(|V|^2)
    """
    dist: dict[V, dict[V, float]] = {}
    for u in graph:
        dist[u] = {}
        for v in graph:
            if u == v:
                dist[u][v] = 0
            elif graph.has_edge(u, v):
                dist[u][v] = graph[u][v].weight
            else:
                dist[u][v] = Graph.INFINITY

    # check vertex k against all other vertices (i, j)
    for k in graph:
        for i in graph:
            for j in graph:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
