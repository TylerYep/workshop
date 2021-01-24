from __future__ import annotations

from collections.abc import Hashable, Iterator
from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class DisjointSetNode(Generic[T]):
    data: T
    index: int
    rank: int = 0
    size: int = 1

    def __post_init__(self) -> None:
        self.parent = self

    def __hash__(self) -> int:
        return hash(self.data)


@unique
class UnionMode(Enum):
    SIZE = auto()
    RANK = auto()
    INDEX = auto()


@dataclass(init=False, repr=False)
class DisjointSet(Generic[T]):
    """
    Implementation of DisjointSet used in Kruskal's algorithm as a union-find data
    structure. Let # of elements n and a(n) be the inverse Ackermann function.

    Runtime:
        Find: O(a(n))
        Union: O(a(n))

    Space: O(n)
    """

    mode: UnionMode

    def __init__(self, *, mode: UnionMode = UnionMode.INDEX) -> None:
        self.node_data: list[DisjointSetNode[T]] = []
        self.data_to_index: dict[T, int] = {}
        self.mode = mode
        self.num_roots = 0

    def __len__(self) -> int:
        return self.num_roots

    def __contains__(self, item: T) -> bool:
        return item in self.data_to_index

    def __bool__(self) -> bool:
        return bool(self.node_data)

    def __iter__(self) -> Iterator[T]:
        for node in self.node_data:
            yield node.data

    def __getitem__(self, elem: T) -> DisjointSetNode[T]:
        return self.node_data[self.data_to_index[elem]]

    def __repr__(self) -> str:
        return f"DisjointSet({self.itersets()})"

    def make_set(self, elem: T) -> None:
        """
        make x as a set.
        rank is the distance from x to its' parent
        root's rank is 0
        """
        if not isinstance(elem, Hashable):
            raise KeyError(f"Element is not a hashable type: {elem}")
        if elem not in self.data_to_index:
            new_node_index = len(self.node_data)
            node = DisjointSetNode(elem, new_node_index)
            self.node_data.append(node)
            self.data_to_index[elem] = new_node_index
            self.num_roots += 1

    def find_set(self, elem: T) -> T:
        """
        Returns the root parent of x using path splitting, which was proven by
        Patwary, Mostofa Ali et al. to be the most efficient variant.
        https://algocoding.wordpress.com/2015/05/13/simple-union-find-techniques/
        """
        if elem not in self.data_to_index:
            raise KeyError(f"Disjoint set does not contain element: {elem}")
        x = self[elem]
        while x != x.parent:
            x, x.parent = x.parent, x.parent.parent
        return x.data

    def union(self, a: T, b: T) -> None:
        """
        Union two sets. Make the set with bigger rank the parent, so that the
        disjoint set tree will be more flat.
        Returns True if two sets were merges, False otherwise.
        """
        a, b = self.find_set(a), self.find_set(b)
        if a == b:
            return
        x, y = self[a], self[b]

        if self.mode is UnionMode.SIZE:
            if x.size < y.size:
                x, y = y, x
            y.parent = x
            x.size += y.size

        elif self.mode is UnionMode.RANK:
            if x.rank < y.rank:
                x, y = y, x
            y.parent = x
            if x.rank == y.rank:
                x.rank += 1

        elif self.mode is UnionMode.INDEX:
            if self.data_to_index[a] < self.data_to_index[b]:
                x.parent = y.parent
            else:
                y.parent = x.parent

        self.num_roots -= 1

    def is_connected(self, x: T, y: T) -> bool:
        """
        :param x: first element
        :param y: second element
        :return: True if x and y belong to the same tree
            (i.e. they have the same root), False otherwise.
        """
        return self.find_set(x) == self.find_set(y)

    def itersets(self) -> list[set[T]]:
        """
        Yields sets of connected components.
        The roots dict shares the set references with entries in the same set.
        """
        roots: dict[T, set[T]] = {}
        seen_nodes: dict[DisjointSetNode[T], T] = {}
        for node in self.node_data:
            curr = node

            unseen_nodes = set()
            cached = False
            while curr != curr.parent:
                if curr in seen_nodes:
                    root = seen_nodes[curr]
                    roots[root].add(node.data)
                    cached = True
                    break
                unseen_nodes.add(curr)
                curr = curr.parent

            root = curr.data
            for new_node in unseen_nodes:
                seen_nodes[new_node] = root

            if not cached:
                if root not in roots:
                    roots[root] = set()
                roots[root].add(node.data)
        return list(roots.values())

    def naive_itersets(self) -> list[set[T]]:
        """
        Yields sets of connected components.
        The roots dict shares the set references with entries in the same set.
        """
        roots: dict[T, set[T]] = {}
        for node in self.node_data:
            curr = node
            while curr != curr.parent:
                curr = curr.parent

            root = curr.data
            if root not in roots:
                roots[root] = set()
            roots[root].add(node.data)
        return list(roots.values())
