from src.structures import DisjointSet, Graph, V


def kruskals(graph: Graph[V]) -> Graph[V]:
    """
    Kruskal's MST Algorithm.
    Not 100% deterministic because edges with the same weight
    are arbitrarily ordered.
    """
    mst = Graph[V](is_directed=False)
    if len(graph) <= 1:
        return mst

    edge_queue = sorted(graph.edges, reverse=True, key=lambda e: e.weight)
    disjoint_sets = DisjointSet[V]()
    for node in graph:
        mst.add_node(node)
        disjoint_sets.make_set(node)

    num_sets = len(disjoint_sets)
    while num_sets != 1:
        edge = edge_queue.pop()
        orig_num_sets = num_sets
        disjoint_sets.union(edge.start, edge.end)
        num_sets = len(disjoint_sets)
        if num_sets < orig_num_sets:
            mst.add_edge(**edge)
    return mst
