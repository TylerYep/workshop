from typing import Set, TypeVar

from src.structures import DisjointSet, Edge, Graph

V = TypeVar("V")


def kruskals(graph: Graph[V]) -> Set[Edge[V]]:
    """
    Kruskal's MST Algorithm.
    Not 100% deterministic because edges with the same weight
    are arbitrarily ordered.
    """
    edge_queue = sorted(graph.edges, reverse=True, key=lambda e: e.weight)
    disjoint_sets = DisjointSet[V]()
    for node in graph:
        disjoint_sets.make_set(node)

    mst = set()
    num_sets = len(disjoint_sets)
    while num_sets != 1:
        edge = edge_queue.pop()
        orig_num_sets = num_sets
        disjoint_sets.union(edge.start, edge.end)
        num_sets = len(disjoint_sets)
        if num_sets < orig_num_sets:
            mst.add(edge)
    return mst
