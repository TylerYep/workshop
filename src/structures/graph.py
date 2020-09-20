from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    KeysView,
    List,
    Optional,
    Sequence,
    TypeVar,
)

from dataslots import with_slots

from src.util import formatter

V = TypeVar("V")


@dataclass(init=False)
class Graph(Generic[V]):
    """
    Use a Dict of Dicts to avoid storing nodes with no edges, as well as
    provide instant lookup for nodes and their neighbors.

    Designed for extensibility - a user can easily add/extend a
    custom Node or Edge class and include it in the type checking system.
    """

    INFINITY = float("inf")
    _graph: Dict[V, Dict[V, Edge[V]]]
    is_directed: bool

    def __init__(
        self, graph: Optional[Dict[V, Dict[V, Any]]] = None, is_directed: bool = True
    ) -> None:
        self.is_directed = is_directed
        self._graph = {} if graph is None else graph
        if graph is not None:
            for u in graph:
                for v in graph[u]:
                    if isinstance(graph[u][v], Edge):
                        continue
                    if isinstance(graph[u][v], dict):
                        graph[u][v] = Edge(u, v, **graph[u][v])
                    elif isinstance(graph[u][v], (int, float)):
                        graph[u][v] = Edge(u, v, weight=graph[u][v])
                    else:
                        raise TypeError(f"{graph[u][v]} is not a supported Edge type.")

    def __str__(self) -> str:
        return str(formatter.pformat(self._graph))

    def __len__(self) -> int:
        return len(self._graph)

    def __bool__(self) -> bool:
        return bool(self._graph)

    def __contains__(self, v_id: V) -> bool:
        return v_id in self._graph

    def __getitem__(self, v_id: V) -> Dict[V, Edge[V]]:
        self.verify_nodes_exist(v_id)
        return self._graph[v_id]

    def __iter__(self) -> Iterator[V]:
        yield from self._graph

    @property
    def nodes(self) -> KeysView[V]:
        return self._graph.keys()

    @property
    def edges(self) -> List[Edge[V]]:
        return [
            self._graph[v_id1][v_id2]
            for v_id1 in self._graph
            for v_id2 in self._graph[v_id1]
        ]

    @classmethod
    def from_graph(
        cls,
        graph: Graph[V],
        node_fn: Callable[[V], Any] = lambda x: x,
        edge_fn: Callable[[Edge[V]], Edge[V]] = lambda x: x,
    ) -> Graph[Any]:
        """
        This function is used to make a copy of a graph, or to apply transformations
        and return a new version of the graph.
        We manually copy the contents of the graph in order to avoid sharing the
        same references to neighbor dicts.
        """
        new_graph: Graph[Any] = Graph({}, is_directed=graph.is_directed)
        for u in graph:
            new_graph.add_node(node_fn(u))
        for u in graph:
            for v in graph[u]:
                new_u, new_v = node_fn(u), node_fn(v)
                edge = edge_fn(graph[u][v])
                new_graph.add_edge(new_u, new_v, weight=edge.weight, **edge.kwargs)
        return new_graph

    @classmethod
    def from_iterable(
        cls,
        iterable: Dict[V, Iterable[V]],
        is_directed: bool = False,
        weight: float = 1,
        **kwargs: Any,
    ) -> Graph[V]:
        graph = {
            node: {
                neighbor: Edge(node, neighbor, weight, **kwargs)
                for neighbor in iterable[node]
            }
            for node in iterable
        }
        return Graph(graph, is_directed=is_directed)

    @classmethod
    def from_matrix(cls, matrix: Sequence[Sequence[float]]) -> Graph[int]:
        is_directed = False
        n = len(matrix)
        graph: Dict[int, Dict[int, float]] = {i: {} for i in range(n)}
        for i in range(n):
            for j in range(n):
                edge_data = matrix[i][j]
                # If matrix is not symmetric, graph is directed
                if not is_directed and i < j and edge_data != matrix[j][i]:
                    is_directed = True
                # Only add edges with nonzero edges.
                if edge_data != Graph.INFINITY:
                    graph[i][j] = edge_data
        return Graph(graph, is_directed=is_directed)

    def to_matrix(self) -> List[List[float]]:
        nodes = sorted(self.nodes)
        graph = [[Graph.INFINITY for _ in nodes] for _ in nodes]
        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):
                if v in self._graph[u]:
                    graph[i][j] = self._graph[u][v].weight
        return graph

    def verify_nodes_exist(self, *v_ids: V) -> None:
        """ Checks existence of provided nodes. """
        for v_id in v_ids:
            if v_id not in self._graph:
                raise KeyError(f"Node not found: {v_id}")

    def adj(self, v_id: V) -> KeysView[V]:
        self.verify_nodes_exist(v_id)
        return self._graph[v_id].keys()

    def degree(self, v_id: V) -> int:
        """
        Returns the total number of edges going in or out of a node.
        For undirected graphs, counts each edge only once.
        """
        self.verify_nodes_exist(v_id)
        if self.is_directed:
            return self.out_degree(v_id) + self.in_degree(v_id)
        return len(self._graph[v_id])

    def out_degree(self, v_id: V) -> int:
        if not self.is_directed:
            raise NotImplementedError("Graph is undirected; use degree() instead.")
        self.verify_nodes_exist(v_id)
        return len(self._graph[v_id])

    def in_degree(self, v_id: V) -> int:
        """
        Iterate all neighbors to see whether any of them reference the current node.
        """
        if not self.is_directed:
            raise NotImplementedError("Graph is undirected; use degree() instead.")
        self.verify_nodes_exist(v_id)
        return sum(v_id in self._graph[node] and v_id != node for node in self._graph)

    def add_node(self, v_id: V) -> None:
        """ You cannot add the same node twice. """
        if v_id in self._graph:
            raise KeyError(f"Node already exists: {v_id}")
        self._graph[v_id] = {}

    def add_edge(self, v_id1: V, v_id2: V, weight: float = 1, **kwargs: Any) -> None:
        """
        For directed graphs, connects the edge v_id1 -> v_id2.
        For undirected graphs, also connects the edge v_id2 -> v_id1.
        Replaces the edge if it already exists.
        """
        self.verify_nodes_exist(v_id1, v_id2)
        edge = Edge(v_id1, v_id2, weight, **kwargs)
        self._graph[v_id1][v_id2] = edge
        if not self.is_directed:
            self._graph[v_id2][v_id1] = edge

    def remove_node(self, v_id: V) -> None:
        """
        Removes all of the edges associated with the v_id node too.
        """
        self.verify_nodes_exist(v_id)
        if self.is_directed:
            for node in self._graph:
                # Make a list copy to avoid removing-while-iterating errors.
                for neighbor in list(self._graph[node]):
                    if v_id in (node, neighbor):
                        del self._graph[node][neighbor]
            del self._graph[v_id]
        else:
            removed_node_dict = self._graph.pop(v_id)
            for neighbor in removed_node_dict:
                if v_id in self._graph[neighbor]:
                    del self._graph[neighbor][v_id]

    def remove_edge(self, v_id1: V, v_id2: V) -> None:
        self.verify_nodes_exist(v_id1, v_id2)
        if v_id2 in self._graph[v_id1]:
            del self._graph[v_id1][v_id2]

    def is_bipartite(self) -> bool:
        """
        Check whether Graph is bipartite using DFS.
        Should not be a property because the calculation changes and
        this should not be thought of as an easily accessible attribute.
        """
        visited = set()
        color: Dict[V, bool] = {}

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


@dataclass(init=False)
class Edge(Generic[V]):
    """ The edge class that stores edge data. """

    start: V
    end: V
    weight: float

    def __init__(self, start: V, end: V, weight: float = 1, **kwargs: Any):
        self.start = start
        self.end = end
        self.weight = weight
        self.kwargs = kwargs

    def __getitem__(self, attr: str) -> Any:
        return self.kwargs[attr]

    def __setitem__(self, attr: str, value: Any) -> None:
        self.kwargs[attr] = value

    def __repr__(self) -> str:
        """ Does not show weight if weight is None. """
        result = str(formatter.pformat(self))[:-1]
        for key, kwarg in self.kwargs.items():
            result += f", {key}={kwarg}"
        return result + ")"

    def __hash__(self) -> int:
        return hash((self.start, self.end))


@with_slots
@dataclass
class Node(Generic[V]):
    """ An example node class that stores node data. """

    data: V

    def __hash__(self) -> int:
        return hash(self.data)
