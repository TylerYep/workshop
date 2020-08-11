from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Generic, Iterable, Iterator, KeysView, List, Optional, TypeVar, cast

import prettyprinter
from prettyprinter.prettyprinter import IMPLICIT_MODULES

prettyprinter.install_extras(include=frozenset({"python", "dataclasses"}))
IMPLICIT_MODULES.add("src.structures.graph")
V = TypeVar("V")
E = TypeVar("E")


@dataclass(repr=False)
class Graph(Generic[V, E]):
    """
    Use a Dict of Dicts to avoid storing nodes with no edges, as well as provide instant
    lookup for nodes and their neighbors.

    Designed for extensibility - a user can easily add/extend a custom Node or Edge class
    and include it in the type checking system.
    """

    _graph: Dict[V, Dict[V, E]] = field(default_factory=dict)
    is_directed: bool = True

    def __len__(self) -> int:
        return len(self._graph)

    def __bool__(self) -> bool:
        return bool(self._graph)

    def __contains__(self, v_id: V) -> bool:
        return v_id in self._graph

    def __getitem__(self, v_id: V) -> Dict[V, E]:
        self.exists_node(v_id)
        return self._graph[v_id]

    def __iter__(self) -> Iterator[V]:
        yield from self._graph

    def __repr__(self) -> str:
        return str(prettyprinter.pformat(self._graph))

    @property
    def nodes(self) -> KeysView[V]:
        return self._graph.keys()

    @property
    def edges(self) -> List[E]:
        return [self._graph[v_id1][v_id2] for v_id1 in self._graph for v_id2 in self._graph[v_id1]]

    @classmethod
    def from_iterable(cls, iterable: Dict[V, Iterable[V]], default_val: Any = None) -> Graph[V, E]:
        if default_val is None:
            default_val = 1
        else:
            cast(E, default_val)
        return Graph(
            {node: {neighbor: default_val for neighbor in iterable[node]} for node in iterable}
        )

    def exists_node(self, *v_ids: V) -> None:
        """ Checks existence of provided nodes. """
        for v_id in v_ids:
            if v_id not in self._graph:
                raise KeyError(f"Node not found: {v_id}")

    def adj(self, v_id: V) -> KeysView[V]:
        self.exists_node(v_id)
        return self._graph[v_id].keys()

    def degree(self, v_id: V) -> int:
        """
        Returns the total number of edges going in or out of a node.
        For undirected graphs, counts each edge only once.
        """
        self.exists_node(v_id)
        if self.is_directed:
            return self.out_degree(v_id) + self.in_degree(v_id)
        return len(self._graph[v_id])

    def out_degree(self, v_id: V) -> int:
        if not self.is_directed:
            raise NotImplementedError("Graph is undirected; use degree() instead.")
        self.exists_node(v_id)
        return len(self._graph[v_id])

    def in_degree(self, v_id: V) -> int:
        """
        Iterate all neighbors to see whether any of them reference the current node.
        """
        if not self.is_directed:
            raise NotImplementedError("Graph is undirected; use degree() instead.")
        self.exists_node(v_id)
        return sum(v_id in self._graph[node] and v_id != node for node in self._graph)

    def add_node(self, v_id: V) -> None:
        """ You cannot add the same node twice. """
        if v_id in self._graph:
            raise KeyError(f"Node already exists: {v_id}")
        self._graph[v_id] = {}

    def add_edge(self, v_id1: V, v_id2: V, edge: Any = None) -> None:
        """
        For directed graphs, connects the edge v_id1 -> v_id2.
        For undirected graphs, also connects the edge v_id2 -> v_id1.
        Replaces the edge if it already exists.
        """
        if edge is not None:
            cast(E, edge)
        self.exists_node(v_id1, v_id2)
        self._graph[v_id1][v_id2] = edge
        if not self.is_directed:
            self._graph[v_id2][v_id1] = edge

    def remove_node(self, v_id: V) -> None:
        """
        Removes all of the edges associated with the v_id node too.
        """
        self.exists_node(v_id)
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
        self.exists_node(v_id1, v_id2)
        if v_id2 in self._graph[v_id1]:
            del self._graph[v_id1][v_id2]


@dataclass
class Node(Generic[V]):
    """ An example node class that stores node data. """

    data: V

    def __hash__(self) -> int:
        return hash(self.data)


@dataclass(repr=False)
class Edge(Generic[V]):
    """ An example edge class that stores edge data. """

    start: V
    end: V
    weight: Optional[float] = None

    def __repr__(self) -> str:
        """ Does not show weight if weight is None. """
        return str(prettyprinter.pformat(self))
