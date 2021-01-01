from cs.structures import DisjointSet, Graph, V


def kruskals_mst(graph: Graph[V]) -> Graph[V]:
    """
    Kruskal's Algorithm to find an MST.
    Not 100% deterministic because edges with the same weight are arbitrarily ordered.

    Kruskal's algorithm sorts all of the graph's edges in ascending order of size, then
    adds one at a time back to a new graph. It maintains a union-find data structure to
    prevent edge additions that would add a cycle to the new graph. Using a union-find
    structure for this gives a worse runtime worse than the O(|E| + |V| log |V|)
    guarantee of Prim's algorithm. However, Prim's algorithm relies on the often slower
    Fibonacci heap, and so Kruskal's algorithm is often faster in practice.

    Runtime: O(|E| log |V|)
    """
    mst = Graph[V](is_directed=False)
    if len(graph) <= 1:
        return mst

    edge_queue = sorted(graph.edges, reverse=True, key=lambda e: e.weight)
    disjoint_sets = DisjointSet[V]()
    for v in graph:
        mst.add_node(v)
        disjoint_sets.make_set(v)

    num_sets = len(disjoint_sets)
    while num_sets != 1:
        edge = edge_queue.pop()
        orig_num_sets = num_sets
        disjoint_sets.union(edge.start, edge.end)
        num_sets = len(disjoint_sets)
        if num_sets < orig_num_sets:
            mst.add_edge(**edge)
    return mst
