from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, KeysView, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from cs.util import Comparable, formatter

V = TypeVar("V", bound=Comparable)


@dataclass(init=False)
class Graph(Generic[V]):
    """
    Use a Dict of Dicts to avoid storing nodes with no edges, as well as
    provide instant lookup for nodes and their neighbors.

    Designed for extensibility - a user can easily add/extend a
    custom Node or Edge class and include it in the type checking system.
    """

    INFINITY = float("inf")
    INT_INFINITY = 1 << 20
    _graph: dict[V, dict[V, Edge[V]]]
    is_directed: bool

    def __init__(
        self,
        graph: dict[V, Any] | None = None,
        *,
        is_directed: bool = True,
        weight: float = 1,
        **kwargs: Any,
    ) -> None:
        """Default constructor assumes an adjacency list representation."""
        self.is_directed = is_directed
        self._graph = {}
        if graph is not None:
            for u in graph:
                self.add_node(u)
            for u in graph:
                for v in graph[u]:
                    if v not in self._graph:
                        self.add_node(v)
                    if isinstance(graph[u], dict):
                        edge = graph[u][v]
                        if isinstance(edge, Edge):
                            self.add_edge(**edge)
                        elif isinstance(edge, dict):
                            self.add_edge(u, v, **edge)
                        elif isinstance(edge, (int, float)):
                            self.add_edge(u, v, weight=edge, **kwargs)
                        else:
                            raise TypeError(f"{edge} is not a supported Edge type.")
                    elif isinstance(graph[u], (list, tuple, set, frozenset)):
                        # Values are some other collection; only contains node names.
                        # Use default weight parameter.
                        self.add_edge(u, v, weight)
                    else:
                        raise TypeError(f"{graph[u]} is not a supported Edge mapping.")

    def __str__(self) -> str:
        return str(formatter.pformat(self._graph))

    def __len__(self) -> int:
        return len(self._graph)

    def __bool__(self) -> bool:
        return bool(self._graph)

    def __contains__(self, v: V) -> bool:
        return v in self._graph

    def __getitem__(self, v: V) -> dict[V, Edge[V]]:
        self.verify_nodes_exist(v)
        return self._graph[v]

    def __iter__(self) -> Iterator[V]:
        yield from self._graph

    @property
    def nodes(self) -> KeysView[V]:
        return self._graph.keys()

    @property
    def edges(self) -> tuple[Edge[V], ...]:
        return tuple(self._graph[u][v] for u in self._graph for v in self._graph[u])

    @classmethod
    def from_graph(
        cls,
        graph: Graph[V],
        *,
        is_directed: bool = True,
        node_fn: Callable[[V], Any] = lambda x: x,
        edge_fn: Callable[[Edge[V]], Edge[V]] = lambda x: x,
    ) -> Graph[Any]:
        """
        This function is used to make a copy of a graph, or to apply transformations
        and return a new version of the graph.
        We manually copy the contents of the graph in order to avoid sharing the
        same references to neighbor dicts.
        """
        new_graph = Graph[Any](is_directed=is_directed)
        for u in graph:
            new_graph.add_node(node_fn(u))
        for u in graph:
            for v in graph[u]:
                new_u, new_v = node_fn(u), node_fn(v)
                edge = edge_fn(graph[u][v])
                new_graph.add_edge(new_u, new_v, edge.weight, **edge.kwargs)
        return new_graph

    @classmethod
    def from_edgelist(
        cls, edge_list: Iterable[Edge[V]], *, is_directed: bool = True
    ) -> Graph[V]:
        graph = Graph[V](is_directed=is_directed)
        for edge in edge_list:
            if edge.start not in graph:
                graph.add_node(edge.start)
            if edge.end not in graph:
                graph.add_node(edge.end)
            graph.add_edge(**edge)
        return graph

    @classmethod
    def from_matrix(
        cls, matrix: Sequence[Sequence[float]], *, zero_is_no_edge: bool = True
    ) -> Graph[int]:
        """By default, treat edges with weight 0 as non-existent edges."""
        is_directed = False
        n = len(matrix)
        graph: dict[int, dict[int, float]] = {i: {} for i in range(n)}
        for i in range(n):
            for j in range(n):
                edge_data = matrix[i][j]
                # If matrix is not symmetric, graph is directed
                if not is_directed and i < j and edge_data != matrix[j][i]:
                    is_directed = True
                # Only add edges with nonzero edges.
                if edge_data != Graph.INFINITY and not (
                    zero_is_no_edge and edge_data == 0
                ):
                    graph[i][j] = edge_data
        return Graph(graph, is_directed=is_directed)

    @staticmethod
    def is_undirected(graph: Any) -> bool:
        """
        Returns whether the graph can be interpreted as undirected - in other words,
        all forward edges have an accompanying reverse edge.
        """
        if not graph:
            return False
        for u in graph:
            for v in graph[u]:
                if u not in graph[v]:
                    return False
        return True

    def to_graphviz(self, img_format: str = "png") -> None:
        from graphviz import Graph as GraphViz  # type: ignore[import]

        dot = GraphViz(format=img_format)
        for node in self.nodes:
            dot.node(str(node))
        for edge in self.edges:
            dot.edge(str(edge.start), str(edge.end))
        dot.render()

    def to_matrix(self, *, zero_is_no_edge: bool = True) -> list[list[float]]:
        """By default, outputs non-existent edges as having weight 0."""
        nodes = sorted(self._graph)
        graph = [
            [0 if zero_is_no_edge else Graph.INFINITY for _ in nodes] for _ in nodes
        ]
        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):
                if v in self._graph[u]:
                    graph[i][j] = self._graph[u][v].weight
        return graph

    def verify_nodes_exist(self, *v_ids: V) -> None:
        """Checks existence of provided nodes."""
        for v in v_ids:
            if v not in self._graph:
                raise KeyError(f"Node not found: {v}")

    def adj(self, v: V) -> KeysView[V]:
        """Used for getting the neighbors of a node in a list-like form."""
        self.verify_nodes_exist(v)
        return self._graph[v].keys()

    def degree(self, v: V) -> int:
        """
        Returns the total number of edges going in or out of a node.
        For undirected graphs, counts each edge only once.
        """
        self.verify_nodes_exist(v)
        if self.is_directed:
            return self.out_degree(v) + self.in_degree(v)
        return len(self._graph[v])

    def out_degree(self, v: V) -> int:
        if not self.is_directed:
            raise NotImplementedError("Graph is undirected; use degree() instead.")
        self.verify_nodes_exist(v)
        return len(self._graph[v])

    def in_degree(self, v: V) -> int:
        """Iterate over neighbors to see whether any reference the current node."""
        if not self.is_directed:
            raise NotImplementedError("Graph is undirected; use degree() instead.")
        self.verify_nodes_exist(v)
        return sum(v in self._graph[node] and v != node for node in self._graph)

    def add_node(self, v: V) -> None:
        """You cannot add the same node twice."""
        if v in self._graph:
            raise KeyError(f"Node already exists: {v}")
        self._graph[v] = {}

    def add_edge(self, start: V, end: V, weight: float = 1, **kwargs: Any) -> None:
        """
        For directed graphs, connects the edge start -> end.
        For undirected graphs, also connects the edge end -> start.
        Replaces the edge if it already exists.

        Note that the function variable names must match the Edge class constructor.
        """
        self.verify_nodes_exist(start, end)
        self._graph[start][end] = Edge(start, end, weight, **kwargs)
        if not self.is_directed:
            # pylint: disable=arguments-out-of-order
            self._graph[end][start] = Edge(end, start, weight, **kwargs)

    def has_edge(self, start: V, end: V) -> bool:
        return start in self._graph and end in self._graph[start]

    def remove_node(self, v: V) -> None:
        """
        Removes all of the edges associated with the node v too.
        """
        self.verify_nodes_exist(v)
        if self.is_directed:
            for node in self._graph:
                # Make a list copy to avoid removing-while-iterating errors.
                for neighbor in list(self._graph[node]):
                    if v in (node, neighbor):
                        del self._graph[node][neighbor]
            del self._graph[v]
        else:
            removed_node_dict = self._graph.pop(v)
            for neighbor in removed_node_dict:
                if v in self._graph[neighbor]:
                    del self._graph[neighbor][v]

    def remove_edge(self, start: V, end: V) -> None:
        self.verify_nodes_exist(start, end)
        if end in self._graph[start]:
            del self._graph[start][end]
            if not self.is_directed:
                del self._graph[end][start]

    def is_bipartite(self) -> bool:
        """
        Check whether Graph is bipartite using DFS.
        Should not be a property because the calculation changes and
        this should not be thought of as an easily accessible attribute.

        The algorithm works by exploring nodes in a DFS fashion and marking the parity
        of each node. As an optimization, we combine this into the depth-first search
        code. If we ever explore an arc where both nodes are known to have the same
        parity, we have detected an odd cycle and return False. Since the DFS considers
        each arc in the graph twice (once in each direction), we're guaranteed that we
        will locate such an edge if it exists.

        Runtime: O(|V| + |E|)
        """
        visited = set()
        color: dict[V, bool] = {}

        def dfs(v: V, curr_color: bool) -> None:
            visited.add(v)
            color[v] = curr_color
            for u in self._graph[v]:
                if u not in visited:
                    dfs(u, not curr_color)

        for node in self._graph:
            if node not in visited:
                dfs(node, True)
        for i in self._graph:
            for j in self._graph[i]:
                if color[i] == color[j]:
                    return False
        return True


@dataclass(init=False, repr=False, order=True)
class Edge(Generic[V], Mapping[str, Any]):
    """
    The edge class that stores edge data.
    Edges are given sort order using start, end, and weight.
    """

    start: V
    end: V
    weight: float

    def __init__(self, start: V, end: V, weight: float = 1, **kwargs: Any):
        self.start = start
        self.end = end
        self.weight = weight
        self.kwargs = kwargs

    def __len__(self) -> int:
        return 3 + len(self.kwargs)

    def __iter__(self) -> Iterator[Any]:
        yield from ("start", "end", "weight")
        yield from self.kwargs

    def __getitem__(self, attr: str) -> Any:
        if attr == "start":
            return self.start
        if attr == "end":
            return self.end
        if attr == "weight":
            return self.weight
        return self.kwargs[attr]

    def __setitem__(self, attr: str, value: Any) -> None:
        if attr == "start":
            self.start = value
        if attr == "end":
            self.end = value
        if attr == "weight":
            self.weight = value
        self.kwargs[attr] = value

    def __repr__(self) -> str:
        result = str(formatter.pformat(self))[:-1]
        for key, kwarg in self.kwargs.items():
            result += f", {key}={kwarg}"
        return result + ")"

    def __hash__(self) -> int:
        return hash((self.start, self.end))


@dataclass(order=True, slots=True)
class Node(Generic[V]):
    """An example node class that stores node data."""

    data: V

    def __hash__(self) -> int:
        return hash(self.data)


class DirectedGraph(Generic[V], Graph[V]):
    def __init__(self, graph: dict[V, Any] | None = None) -> None:
        super().__init__(graph)


class UndirectedGraph(Generic[V], Graph[V]):
    def __init__(self, graph: dict[V, Any] | None = None) -> None:
        super().__init__(graph, is_directed=False)
