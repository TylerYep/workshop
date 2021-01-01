from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, Optional, TypeVar

from dataslots import dataslots

from cs.util import Comparable, formatter

T = TypeVar("T", bound=Comparable)


@dataslots
@dataclass(order=True, repr=False)
class TreeNode(Generic[T]):
    data: T

    def __repr__(self) -> str:
        return str(formatter.pformat(self))


@dataclass(init=False)
class Tree(Generic[T]):
    """
    We separate the BinarySearchTree with the TreeNode class to allow the root
    of the tree to be None, which allows this implementation to type-check.
    """

    root: Optional[TreeNode[T]] = None
    size: int = 0

    def __bool__(self) -> bool:
        return self.root is not None

    def __contains__(self, data: T) -> bool:
        return self.search(data) is not None

    def __iter__(self) -> Iterator[TreeNode[T]]:
        raise NotImplementedError

    def __len__(self) -> int:
        return self.size

    def clear(self) -> None:
        raise NotImplementedError

    def search(self, data: T) -> Optional[TreeNode[T]]:
        raise NotImplementedError

    def insert(self, data: T) -> None:
        raise NotImplementedError

    def remove(self, data: T) -> None:
        raise NotImplementedError

    def max_element(self) -> T:
        raise NotImplementedError

    def min_element(self) -> T:
        raise NotImplementedError

    def traverse(self, method: str = "inorder") -> Iterator[T]:
        raise NotImplementedError
