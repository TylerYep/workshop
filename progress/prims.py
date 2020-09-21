# from typing import Any, Dict, TypeVar
# from src.structures import Graph

# V = TypeVar("V")


# def prim(graph: Graph[V], start: V) -> Dict[V, float]:
#     """
#     Prim's MST Algorithm
#         Args :  G - Dictionary of edges
#                 s - Starting Node
#         Vars :  distances - Dictionary storing shortest distance
#                         from s to nearest node
#                 visited - Set of visited nodes
#                 path - Preceding node in path
#     """
#     distances = {start: 0}
#     visited = set()
#     path = {start: 0}
#     while len(visited) != len(graph) - 1:
#         mini = 100000
#         for v in distances:
#             if v not in visited and distances[v] < mini:
#                 mini = distances[v]
#                 u = v
#         visited.add(u)
#         for edge in graph[u].values():
#             if edge.start not in visited:
#                 if edge.end < distances.get(edge.start, 100000):
#                     distances[edge.start] = edge.end
#                     path[edge.start] = start
#     return distances
