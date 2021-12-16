from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from cs.util import Comparable, dfield, formatter

T = TypeVar("T", bound=Comparable)


@dataclass(order=True, repr=False, slots=True)
class TreeNode(Generic[T]):
    """
    For inheritance to type-check properly, we will need to re-define any TreeNode
    member variables in subclasses.

    We define all augmented information for nodes within this class. If this information
    is not needed for efficiency reasons, it should be fairly simple to remove any lines
    of code using them. However, the overhead they add is so small that it probably
    wouldn't be worth it.

    count: # of times this node was added
    hits: # of times this node was searched
    rank (RBTree-only): # of nodes smaller than this one
    """

    data: T
    count: int = dfield(1)
    hits: int = dfield(0)

    def __repr__(self) -> str:
        return str(formatter.pformat(self))


@dataclass(init=False)
class Tree(Generic[T]):
    """
    Trees can be extended to have any number of child nodes.

    We separate the BinarySearchTree with the TreeNode class to allow the root
    of the tree to be None, which allows this implementation to type-check.

    We set init=False because a Tree cannot receive any parameters on creation, and we
    omit default values to root and size to prevent Tree from being instantiated.

    Trees cannot use __slots__ because root needs to be assigned on the first insert.
    """

    root: TreeNode[T] | None
    size: int

    def __bool__(self) -> bool:
        return self.root is not None

    def __contains__(self, data: T) -> bool:
        return self.search(data) is not None

    def __iter__(self) -> Iterator[TreeNode[T]]:
        raise NotImplementedError

    def __len__(self) -> int:
        return self.size

    @staticmethod
    def depth(tree: Any) -> int:
        raise NotImplementedError

    def height(self) -> int:
        return self.depth(self.root)

    def clear(self) -> None:
        self.root = None

    def search(self, data: T) -> TreeNode[T] | None:
        raise NotImplementedError

    def insert(self, data: T) -> None:
        raise NotImplementedError

    def remove(self, data: T) -> None:
        raise NotImplementedError

    def is_balanced(self) -> bool:
        raise NotImplementedError

    def max_element(self) -> T:
        raise NotImplementedError

    def min_element(self) -> T:
        raise NotImplementedError

    def traverse(self, method: str = "inorder") -> Iterator[T]:
        raise NotImplementedError

    def select(self, rank: int) -> T:
        raise NotImplementedError

    def rank_of(self, data: T) -> int:
        raise NotImplementedError
