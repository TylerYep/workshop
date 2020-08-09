from dataclasses import dataclass, field
from typing import Any, Dict, Generic, Iterator, KeysView, List, Optional, TypeVar

import prettyprinter
from prettyprinter.prettyprinter import IMPLICIT_MODULES

prettyprinter.install_extras(include=frozenset({"python", "dataclasses", "numpy"}))
IMPLICIT_MODULES.add("src.structures.graph")
V = TypeVar("V")
E = TypeVar("E")
NODE_ERROR = "Node not found: {}"


@dataclass
class Node(Generic[V]):
    v_id: V
    data: Any
    neighbors: List[V] = field(default_factory=list)


@dataclass(repr=False)
class Edge(Generic[V]):
    """ Stores edge data. """

    start: V
    end: V
    weight: Optional[float] = None

    def __repr__(self) -> str:
        """ Does not show weight if weight is None. """
        return str(prettyprinter.pformat(self))


@dataclass(repr=False)
class Graph(Generic[V, E]):
    """
    Use a Dict to avoid storing nodes with no edges.
    Designed for extensibility - can add/extend a custom Node or Edge class
    """

    _graph: Dict[V, Dict[V, Optional[E]]] = field(default_factory=dict)
    is_directed: bool = True

    @property
    def nodes(self) -> KeysView[V]:
        return self._graph.keys()

    @property
    def edges(self) -> List[Optional[E]]:
        return [self._graph[v_id1][v_id2] for v_id1 in self._graph for v_id2 in self._graph[v_id1]]

    def adj(self, v_id: V) -> KeysView[V]:
        if v_id not in self._graph:
            raise KeyError(NODE_ERROR.format(v_id))
        return self._graph[v_id].keys()

    def degree(self, v_id: V) -> int:
        """
        Returns the total number of edges going in or out of a node.
        For undirected graphs, counts each edge only once.
        """
        if v_id not in self._graph:
            raise KeyError(NODE_ERROR.format(v_id))

        if self.is_directed:
            return self.out_degree(v_id) + self.in_degree(v_id)
        return len(self._graph[v_id])

    def out_degree(self, v_id: V) -> int:
        return len(self._graph[v_id])

    def in_degree(self, v_id: V) -> int:
        if self.is_directed:
            return sum(
                v_id in self._graph[neighbor] and v_id != neighbor for neighbor in self._graph[v_id]
            )
        return len(self._graph[v_id])

    def __len__(self) -> int:
        return len(self._graph)

    def __getitem__(self, x: V) -> Dict[V, Optional[E]]:
        return self._graph[x]

    def __iter__(self) -> Iterator[V]:
        yield from self._graph

    def add_node(self, v_id: V) -> None:
        """ You cannot add the same node twice. """
        if v_id in self._graph:
            raise KeyError(f"Node already exists: {v_id}")
        self._graph[v_id] = {}

    def add_edge(self, v_id1: V, v_id2: V, edge: Optional[E] = None) -> None:
        # edge: Optional[E] = None, **kwargs: Any) -> None:
        """
        For directed graphs, connects the edge v_id1 -> v_id2.
        For undirected graphs, also connects the edge v_id2 -> v_id1.
        Replaces the edge if it already exists.
        """
        for v_id in (v_id1, v_id2):
            if v_id not in self._graph:
                raise KeyError(NODE_ERROR.format(v_id))

        self._graph[v_id1][v_id2] = edge
        if not self.is_directed:
            self._graph[v_id2][v_id1] = edge

    def remove_node(self, v_id: V) -> None:
        """
        Removes all of the edges associated with the v_id node too.
        """
        if v_id not in self._graph:
            raise KeyError(NODE_ERROR.format(v_id))

        if self.is_directed:
            for node in self._graph:
                # Make a list copy to avoid removing while iterating errors.
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
        if v_id2 in self._graph[v_id1]:
            del self._graph[v_id1][v_id2]

    def __repr__(self) -> str:
        return str(prettyprinter.pformat(self._graph))
