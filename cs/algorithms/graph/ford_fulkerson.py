from __future__ import annotations

from typing import Any, Iterable, Mapping, cast

from cs.structures import Edge, Graph, V


def bipartite_matching(
    graph: Graph[V], left: Iterable[V] | Mapping[V, int], right: Iterable[V]
) -> tuple[Graph[V], list[Edge[V]]]:
    source = cast(Any, "Source")
    sink = cast(Any, "Sink")
    graph.add_node(source)
    graph.add_node(sink)
    if isinstance(left, Mapping):
        for node, count in left.items():
            graph.add_edge(source, node, weight=count)
    else:
        for node in left:
            graph.add_edge(source, node, weight=1)
    for node in right:
        graph.add_edge(node, sink)

    max_flow_graph = ford_max_flow_network(graph, source, sink)
    matching_edges = [
        edge
        for edge in max_flow_graph.edges
        if edge["flow"] >= 1 and edge.start in left and edge.end in right
    ]
    return max_flow_graph, matching_edges


def ford_max_flow(graph: Graph[V], source: V, sink: V) -> float:
    result = ford_max_flow_network(graph, source, sink)
    return sum(edge["flow"] for edge in result[source].values())


def ford_max_flow_network(graph: Graph[V], source: V, sink: V) -> Graph[V]:
    """
    Given a graph and a pair of nodes s and t, produces a maximum s-t flow in that
    graph. Flow that already exists in the input network will be used as a guess of
    the maximum flow.

    The algorithm works by maintaining a candidate max flow, constructing the residual
    graph for that max flow, and then searching for an augmenting s-t path in the graph.
    If one is found, then the maximum possible flow is pushed along that path and the
    process repeats. Otherwise, no augmenting paths exist, and the flow must be maximum.

    Each time an augmenting path is found, the s-t flow increases by at least one, so
    the algorithm is guaranteed to terminate after at most F searches, where F is the
    value of the max-flow. Since each search to find an augmenting path from s to t
    takes O(m + n), the overall runtime is O((m + n)F).

    Runtime: O((m + n)F)
    """
    flow_network = Graph.from_graph(
        graph, edge_fn=lambda e: Edge(**e, capacity=e.weight, flow=0)
    )
    if source == sink:
        return flow_network

    # Pushing flow across an edge in the original graph is equivalent to retracting flow
    # across an edge in the residual graph. The flow across an edge is represented
    # implicitly by the amount of capacity remaining on its residual edge.
    residual_graph = Graph.from_graph(
        flow_network,
        edge_fn=lambda e: Edge(
            e.start, e.end, capacity=e["capacity"] - e["flow"], is_residual=False
        ),
    )
    # Add all of the reverse edges with capacity equal to the reverse flow.
    for edge in flow_network.edges:
        residual_graph.add_edge(
            edge.end, edge.start, capacity=edge["flow"], is_residual=True
        )

    while True:
        # Find an augmenting s-t path in the residual graph.
        path = find_path(residual_graph, source, sink)
        if path is None:
            break

        # Augments the flow along an augmenting path by the minimum remaining capacity
        # along some edge. Determine the smallest capacity of this path, then push this
        # much flow across all the nodes.
        min_capacity = min(edge["capacity"] for edge in path)
        for edge in path:
            add_flow(residual_graph, edge, min_capacity)

    # We now have a max flow because no augmenting paths are left.  Take the data from
    # our residual graph and use it to fill in the flow in the resulting flow network.
    for u in residual_graph:
        for v, edge in residual_graph[u].items():
            if edge["is_residual"]:
                flow_network[v][u]["flow"] = edge["capacity"]

    return flow_network


def add_flow(graph: Graph[V], edge: Edge[V], amount: int) -> None:
    """
    Adds or subtracts the indicated number of flow units across this edge. If the amount
    of flow added or removed exceeds the capacity of the edge, throws a RuntimeError.
    """
    if amount < 0:
        add_flow(graph, graph[edge.end][edge.start], -amount)
        return

    capacity = edge["capacity"]
    if amount > capacity:
        raise RuntimeError(
            f"Cannot push {amount} units of flow across edge of capacity {capacity}."
        )
    edge["capacity"] -= amount
    graph[edge.end][edge.start]["capacity"] += amount


def find_path(
    residual_graph: Graph[V], start: V, end: V, visited: set[V] | None = None
) -> list[Edge[V]] | None:
    """
    Recursively explores a residual graph, starting at the node indicated by start and
    searching for a particular destination node. If a path is found, it is returned.
    """
    if visited is None:
        visited = set()

    if start in visited:
        return None

    visited.add(start)
    if start == end:
        return []

    for v, edge in residual_graph[start].items():
        if edge["capacity"] == 0:
            continue

        result = find_path(residual_graph, v, end, visited)
        if result is not None:
            result.append(edge)
            return result

    return None
