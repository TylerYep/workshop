# from typing import Any, Dict, TypeVar
# from src.structures import Graph

# V = TypeVar("V")


# def floy(A_and_n):
#     """
#     Floyd Warshall's algorithm
#         Args :  G - Dictionary of edges
#                 s - Starting Node
#         Vars :  dist - Dictionary storing shortest distance from s to every other node
#                 known - Set of knows nodes
#                 path - Preceding node in path
#     """
#     (A, n) = A_and_n
#     dist = list(A)
#     path = [[0] * n for i in range(n)]
#     for k in range(n):
#         for i in range(n):
#             for j in range(n):
#                 if dist[i][j] > dist[i][k] + dist[k][j]:
#                     dist[i][j] = dist[i][k] + dist[k][j]
#                     path[i][k] = k
#     print(dist)


# def floyd_warshall(graph):
#     """
#     :param graph: 2D array calculated from weight[edge[i, j]]
#     :type graph: List[List[float]]
#     :param v: number of vertices
#     :type v: int
#     :return: shortest distance between all vertex pairs
#     distance[u][v] will contain the shortest distance from vertex u to v.

#     1. For all edges from v to n, distance[i][j] = weight(edge(i, j)).
#     3. The algorithm then performs distance[i][j] = min(distance[i][j], distance[i][k] +
#         distance[k][j]) for each possible pair i, j of vertices.
#     4. The above is repeated for each vertex k in the graph.
#     5. Whenever distance[i][j] is given a new minimum value, next vertex[i][j] is
#         updated to the next vertex[i][k].
#     """
#     dist: Dict[V, Dict[V, float]] = {v: {} for v in graph}

#     # dist = [[float("inf") for _ in range(v)] for _ in range(v)]

#     for i in graph:
#         for j in graph:
#             dist[i][j] = graph[i][j]

#     # check vertex k against all other vertices (i, j)
#     for k in graph:
#         # looping through rows of graph array
#         for i in graph:
#             # looping through columns of graph array
#             for j in graph:
#                 if (
#                     dist[i][k] != float("inf")
#                     and dist[k][j] != float("inf")
#                     and dist[i][k] + dist[k][j] < dist[i][j]
#                 ):
#                     dist[i][j] = dist[i][k] + dist[k][j]

#     _print_dist(dist, v)
#     return dist, v
