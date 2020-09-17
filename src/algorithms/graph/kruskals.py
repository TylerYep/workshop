from typing import List, TypeVar

from src.structures import Edge, Graph

V = TypeVar("V")


def kruskals(graph: Graph[V]) -> List[Edge[V]]:
    """
    Kruskal's MST Algorithm
    """
    edge_queue = sorted(graph.edges, reverse=True, key=lambda e: e.weight)
    disjoint_sets = [{node} for node in graph]
    mst = []
    while len(disjoint_sets) != 1:
        edge = edge_queue.pop()
        i = 0
        for set_i in disjoint_sets:
            if edge.start in set_i:
                i += 1
        for j, set_j in enumerate(disjoint_sets):
            if edge.end in set_j:
                if i == j:
                    break
                set_j |= disjoint_sets[i]
                disjoint_sets.pop(i)
                mst.append(edge)
                break
    return mst
