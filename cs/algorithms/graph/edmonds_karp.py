from cs.algorithms import breadth_first_search
from cs.structures import Graph, V


def edmonds_karp_max_flow(graph: Graph[V], source: V, sink: V) -> float:
    flow_network = Graph.from_graph(graph)
    max_flow = 0.0

    # Augment the flow while there is path from source to sink
    while path := breadth_first_search(flow_network, source, sink):
        # Find minimum residual capacity of the edges along the path filled by BFS,
        # aka the maximum flow through the path found, by iterating over pairs of nodes.
        path_flow = min(
            flow_network[path[i]][path[i + 1]].weight for i in range(len(path) - 1)
        )
        max_flow += path_flow

        # Update residual capacities of the edges and reverse edges along the path
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            if u not in flow_network[v]:
                flow_network.add_edge(v, u, 0)
            flow_network[u][v].weight -= path_flow
            flow_network[v][u].weight += path_flow
    return max_flow
