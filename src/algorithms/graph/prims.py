# from typing import Any, Dict, Set
# from src.structures import Graph, V
# import random


# def prims(graph: Graph[V]) -> Dict[V, float]:
#     """
#     Prim's MST Algorithm
#         Args :  G - Dictionary of edges
#                 s - Starting Node
#         Vars :  distances - Dictionary storing shortest distance
#                         from s to nearest node
#                 visited - Set of visited nodes
#                 path - Preceding node in path
#     """
#     start = next(iter(graph))
#     distances = {start: 0}
#     visited: Set[V] = set()
#     path = {start: 0}
#     while len(visited) != len(graph) - 1:
#         mini = Graph.INFINITY
#         for v in distances:
#             if v not in visited and distances[v] < mini:
#                 mini = distances[v]
#                 u = v
#         visited.add(u)
#         for edge in graph[u].values():
#             if edge.start not in visited:
#                 if edge.end < distances.get(edge.start, Graph.INFINITY):
#                     distances[edge.start] = edge.end
#                     path[edge.start] = start
#     return distances
