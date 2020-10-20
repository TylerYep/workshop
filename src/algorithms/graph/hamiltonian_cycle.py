"""
A Hamiltonian cycle (Hamiltonian circuit) is a graph cycle through a graph that visits
each node exactly once. Determining whether such paths and cycles exist in graphs is
the 'Hamiltonian path problem', which is NP-complete. Wikipedia:
https://en.wikipedia.org/wiki/Hamiltonian_path
"""
from typing import List


def hamiltonian_cycle(graph: List[List[int]], start_index: int) -> List[int]:
    """
    Either return array of vertices indicating the hamiltonian cycle
    or an empty list indicating that hamiltonian cycle was not found.
    """

    def _valid_connection(
        graph: List[List[int]], neighbor: int, curr_ind: int, path: List[int]
    ) -> bool:
        """ Checks whether it is possible to add next into path. """
        # Validate that no path exists between current and next vertices
        if graph[path[curr_ind - 1]][neighbor] == 0:
            return False
        # Validate that next vertex is not already in path
        return not any(vertex == neighbor for vertex in path)

    def _hamilton_cycle(graph: List[List[int]], path: List[int], curr_ind: int) -> bool:
        if curr_ind == len(graph):
            # Return whether path exists between current and starting vertices
            return graph[path[curr_ind - 1]][path[0]] == 1

        for neighbor in range(len(graph)):
            if _valid_connection(graph, neighbor, curr_ind, path):
                path[curr_ind] = neighbor
                if _hamilton_cycle(graph, path, curr_ind + 1):
                    return True
                path[curr_ind] = -1
        return False

    path = [-1] * (len(graph) + 1)
    path[0] = start_index
    path[-1] = start_index
    return path if _hamilton_cycle(graph, path, 1) else []
