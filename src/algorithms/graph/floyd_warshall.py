from typing import List

from src.structures import Graph


def floyd_warshall(graph: List[List[float]]) -> List[List[float]]:
    """
    Calculates the shortest distance between all vertex pairs using dynamic programming.
    distance[u][v] will contain the shortest distance from vertex u to v.

    1. For all edges from v to n, distance[i][j] = weight(edge(i, j)).
    3. The algorithm then performs distance[i][j] = min(distance[i][j], distance[i][k]
        + distance[k][j]) for each possible pair i, j of vertices.
    4. The above is repeated for each vertex k in the graph.
    5. Whenever distance[i][j] is given a new minimum value, next vertex[i][j] is
        updated to the next vertex[i][k].

    Unlike Dijkstra's Algorithm, the Floyd-Warshall Algorithm has no problems
    handling graphs with negative edge costs.

    Runtime: O(|V|^3)
    Memory: O(|V|^2)
    """
    n = len(graph)
    dist = [[Graph.INFINITY for _ in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            dist[i][j] = graph[i][j]

    # check vertex k against all other vertices (i, j)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
