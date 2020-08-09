from dataclasses import dataclass, field
from typing import Any, Dict, Generic, Iterator, KeysView, List, Optional, TypeVar

import prettyprinter
from prettyprinter.prettyprinter import IMPLICIT_MODULES

prettyprinter.install_extras(include=frozenset({"python", "dataclasses", "numpy"}))
IMPLICIT_MODULES.add("src.structures.graph")
V_ID = TypeVar("V_ID")
NODE_ERROR = "Node not found: {}"


@dataclass
class Node(Generic[V_ID]):
    v_id: V_ID
    data: Any
    neighbors: List[V_ID] = field(default_factory=list)


@dataclass(repr=False)
class Edge(Generic[V_ID]):
    """ Stores edge data. """

    start: V_ID
    end: V_ID
    weight: Optional[float] = None

    def __repr__(self) -> str:
        """ Does not show weight if weight is None. """
        return str(prettyprinter.pformat(self))


@dataclass(repr=False)
class Graph(Generic[V_ID]):
    """ Use a Dict to avoid storing nodes with no edges. """

    graph: Dict[V_ID, Dict[V_ID, Edge[V_ID]]] = field(default_factory=dict)
    is_directed: bool = True

    @property
    def nodes(self) -> KeysView[V_ID]:
        return self.graph.keys()

    @property
    def edges(self) -> List[Edge[V_ID]]:
        return [self.graph[v_id1][v_id2] for v_id1 in self.graph for v_id2 in self.graph[v_id1]]

    def adj(self, v_id: V_ID) -> KeysView[V_ID]:
        if v_id not in self.graph:
            raise KeyError(NODE_ERROR.format(v_id))
        return self.graph[v_id].keys()

    def degree(self, v_id: V_ID) -> int:
        """
        Returns the total number of edges going in or out of a node.
        For undirected graphs, counts each edge only once.
        """
        if v_id not in self.graph:
            raise KeyError(NODE_ERROR.format(v_id))

        if self.is_directed:
            return self.out_degree(v_id) + self.in_degree(v_id)
        return len(self.graph[v_id])

    def out_degree(self, v_id: V_ID) -> int:
        return len(self.graph[v_id])

    def in_degree(self, v_id: V_ID) -> int:
        if self.is_directed:
            return sum(
                v_id in self.graph[neighbor] and v_id != neighbor for neighbor in self.graph[v_id]
            )
        return len(self.graph[v_id])

    def __len__(self) -> int:
        return len(self.graph)

    def __getitem__(self, x: V_ID) -> Dict[V_ID, Edge[V_ID]]:
        return self.graph[x]

    def __iter__(self) -> Iterator[V_ID]:
        yield from self.graph

    def add_node(self, v_id: V_ID) -> None:
        """ You cannot add the same node twice. """
        if v_id in self.graph:
            raise KeyError(f"Node already exists: {v_id}")
        self.graph[v_id] = {}

    def add_edge(self, v_id1: V_ID, v_id2: V_ID, weight: Optional[float] = None) -> None:
        """
        For directed graphs, connects the edge v_id1 -> v_id2.
        For undirected graphs, also connects the edge v_id2 -> v_id1.
        Replaces the edge if it already exists.
        """
        for v_id in (v_id1, v_id2):
            if v_id not in self.graph:
                raise KeyError(NODE_ERROR.format(v_id))

        self.graph[v_id1][v_id2] = Edge[V_ID](v_id1, v_id2, weight)
        if not self.is_directed:
            self.graph[v_id2][v_id1] = Edge[V_ID](v_id2, v_id1, weight)

    def remove_node(self, v_id: V_ID) -> None:
        """
        Removes all of the edges associated with the v_id node too.
        """
        if v_id not in self.graph:
            raise KeyError(NODE_ERROR.format(v_id))

        if self.is_directed:
            for node in self.graph:
                # Make a list copy to avoid removing while iterating errors.
                for neighbor in list(self.graph[node]):
                    if v_id in (node, neighbor):
                        del self.graph[node][neighbor]
            del self.graph[v_id]

        else:
            removed_node_dict = self.graph.pop(v_id)
            for neighbor in removed_node_dict:
                if v_id in self.graph[neighbor]:
                    del self.graph[neighbor][v_id]

    def remove_edge(self, v_id1: V_ID, v_id2: V_ID) -> None:
        if v_id2 in self.graph[v_id1]:
            del self.graph[v_id1][v_id2]

    def __repr__(self) -> str:
        return str(prettyprinter.pformat(self.graph))
