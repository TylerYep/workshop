"""
A Hamiltonian cycle (Hamiltonian circuit) is a graph cycle through a graph that visits
each node exactly once. Determining whether such paths and cycles exist in graphs is
the 'Hamiltonian path problem', which is NP-complete. Wikipedia:
https://en.wikipedia.org/wiki/Hamiltonian_path
"""
from __future__ import annotations

from typing import cast

from cs.structures import Graph, V


def hamiltonian_cycle(graph: Graph[V], start: V) -> list[V]:
    """
    Either return array of vertices indicating the hamiltonian cycle
    or an empty list indicating that hamiltonian cycle was not found.
    """

    def hamilton_cycle(graph: Graph[V], path: list[V | None], curr_ind: int) -> bool:
        prev = path[curr_ind - 1]
        if prev is None:
            raise RuntimeError

        if curr_ind == len(graph):
            # Return whether path exists between current and starting vertices
            return start in graph[prev]

        for neighbor in graph[prev]:
            if neighbor not in path:
                path[curr_ind] = neighbor
                if hamilton_cycle(graph, path, curr_ind + 1):
                    return True
                path[curr_ind] = None
        return False

    path: list[V | None] = [None] * (len(graph) + 1)
    path[0] = path[-1] = start
    return cast(list[V], path) if hamilton_cycle(graph, path, 1) else []
