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
   [1, 0, 1, 1, 1],
   [0, 1, 0, 0, 1],
   [1, 1, 0, 0, 1],
   [0, 1, 1, 1, 0]]
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
   [1, 0, 1, 1, 1],
   [0, 1, 0, 0, 1],
   [1, 1, 0, 0, 1],
   [0, 1, 1, 1, 0]]
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
   [1, 0, 1, 1, 1],
   [0, 1, 0, 0, 1],
   [1, 1, 0, 0, 0],
   [0, 1, 1, 0, 0]]
>>> hamilton_cycle(graph,4)
[]
"""
