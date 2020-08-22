# from typing import Any, Dict, TypeVar
# from src.structures import Graph

# V = TypeVar("V")


# def prim(G: Graph[Any, float], start: V) -> Dict[V, float]:
#     """
#     Prim's MST Algorithm
#         Args :  G - Dictionary of edges
#                 s - Starting Node
#         Vars :  distances - Dictionary storing shortest distance from s to nearest node
#                 visited - Set of visited nodes
#                 path - Preceding node in path
#     """
#     distances = {start: 0}
#     visited = set()
#     path = {start: 0}
#     while len(visited) != len(G) - 1:
#         mini = 100000
#         for v in distances:
#             if v not in visited and distances[v] < mini:
#                 mini = distances[v]
#                 u = v
#         visited.add(u)
#         for v in G[u]:
#             if v[0] not in visited:
#                 if v[1] < distances.get(v[0], 100000):
#                     distances[v[0]] = v[1]
#                     path[v[0]] = u
#     return distances
