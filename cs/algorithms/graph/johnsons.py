from cs.algorithms import bellman_ford_shortest_paths, dijkstra_shortest_paths
from cs.structures import Edge, Graph, Node, V


def johnsons_shortest_paths(graph: Graph[V]) -> dict[V, dict[V, float]]:
    """
    An implementation of Johnson's all-pairs shortest paths algorithm.  This algorithm
    is remarkable in that it combines two single-source shortest path algrithms -
    Dijkstra's algorithm and the Bellman-Ford algorithm - into a single algorithm for
    all-pairs shortest paths that ends up being more efficient than the Floyd-Warshall
    all-pairs shortest paths algorithm when run on sparse graphs.

    The idea behind Johnson's algorithm is to enforce that all the edge costs in the
    graph are nonnegative by computing a new potential function h(v) for each node in
    the graph, and then creating a new edge cost for each edge. With this new graph, we
    can use Dijkstra's to get the shortest paths.

    Runtime: O(|V||E| + |V|^2 log |V|)
    """
    # Create augmented graph G' that will be fed into the Bellman-Ford algorithm by
    # copying the graph and adding an extra node. Adding a new directed source node
    # ensures that there will be no negative cycles in this new graph. We convert the
    # graph into a Node[tuple[V]] type in order to ensure we can add a new, unique node.
    aug_graph = Graph.from_graph(graph, node_fn=lambda x: Node((x,)))
    source_node = Node(())
    aug_graph.add_node(source_node)
    for u in aug_graph:
        if u != source_node:
            aug_graph.add_edge(source_node, u, 0)

    # Convert the Bellman-Ford output of Node[tuple[V]] back into the original type.
    bellman_costs = {
        node.data[0]: cost
        for node, cost in bellman_ford_shortest_paths(aug_graph, source_node).items()
        if node.data
    }

    # Given a graph and a potential function on that graph (maps nodes to their
    # potentials), produces a new graph whose edges are weighted by the potential.
    reweighted_graph = Graph.from_graph(
        graph,
        edge_fn=lambda e: Edge(
            e.start, e.end, e.weight + bellman_costs[e.start] - bellman_costs[e.end]
        ),
    )

    # Run Dijkstra's algorithm over every node in the reweighted graph
    # to get the transformed shortest path costs.
    return {
        u: {
            v: cost + bellman_costs[v] - bellman_costs[u]
            for v, cost in dijkstra_shortest_paths(reweighted_graph, u).items()
        }
        for u in graph
    }
