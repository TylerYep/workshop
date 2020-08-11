# from typing import Any, Dict, Generic, List

# from dataclasses import dataclass, field

# V_ID = int

# @dataclass
# class Graph:
#     @property
#     def nodes(self) -> List[V_ID]:
#         raise NotImplementedError

#     @property
#     def edges(self) -> List[Edge]:
#         raise NotImplementedError

#     @property
#     def num_nodes(self):
#         raise NotImplementedError


# @dataclass
# class MatrixGraph(Graph):
#     graph: List[List[Node]]
#     V: List[Node]

#     def __post_init__(self) -> None:
#         if len(self.graph) != len(self.graph[0]):
#             raise ValueError("Graph does not have the same # of rows and columns.")

#     @property
#     def nodes(self) -> List[V_ID]:
#         return self.V

#     @property
#     def edges(self) -> List[Edge]:
#         return []

#     def __getitem__(self, x: V_ID) -> List[Node]:
#         return self.V[x]

r"""
Wrapper function to call subroutine called util_hamilton_cycle,
which will either return array of vertices indicating hamiltonian cycle
or an empty list indicating that hamiltonian cycle was not found.
Case 1:
Following graph consists of 5 edges.
If we look closely, we can see that there are multiple Hamiltonian cycles.
For example one result is when we iterate like:
(0)->(1)->(2)->(4)->(3)->(0)

(0)---(1)---(2)
    |   /   \   |
    |  /     \  |
    | /       \ |
    |/         \|
(3)---------(4)
>>> graph = [[0, 1, 0, 1, 0],
...          [1, 0, 1, 1, 1],
...          [0, 1, 0, 0, 1],
...          [1, 1, 0, 0, 1],
...          [0, 1, 1, 1, 0]]
>>> hamilton_cycle(graph)
[0, 1, 2, 4, 3, 0]

Case 2:
Same Graph as it was in Case 1, changed starting index from default to 3

(0)---(1)---(2)
    |   /   \   |
    |  /     \  |
    | /       \ |
    |/         \|
(3)---------(4)
>>> graph = [[0, 1, 0, 1, 0],
...          [1, 0, 1, 1, 1],
...          [0, 1, 0, 0, 1],
...          [1, 1, 0, 0, 1],
...          [0, 1, 1, 1, 0]]
>>> hamilton_cycle(graph, 3)
[3, 0, 1, 2, 4, 3]

Case 3:
Following Graph is exactly what it was before, but edge 3-4 is removed.
Result is that there is no Hamiltonian Cycle anymore.

(0)---(1)---(2)
    |   /   \   |
    |  /     \  |
    | /       \ |
    |/         \|
(3)         (4)
>>> graph = [[0, 1, 0, 1, 0],
...          [1, 0, 1, 1, 1],
...          [0, 1, 0, 0, 1],
...          [1, 1, 0, 0, 0],
...          [0, 1, 1, 0, 0]]
>>> hamilton_cycle(graph,4)
[]
"""
