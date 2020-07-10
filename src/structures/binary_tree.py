from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


class BinaryTree(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[TreeNode[T]] = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[TreeNode[T]]:
        node = self.head
        prev = None
        while node is not None:
            prev = node
            if node.left is not None:
                yield node
                node = node.left
            if node.right is not None:
                yield node
                node = node.right
            node = prev

    # def insert(self, data):
    #     # Compare the new value with the parent node
    #     if self.data:
    #         if data < self.data:
    #             self.left = TreeNode(data) if self.left is None else self.left.insert(data)
    #         elif data > self.data:
    #             self.right = TreeNode(data) if self.right is None else self.right.insert(data)
    #     else:
    #         self.data = data


class TreeNode(Generic[T]):
    def __init__(
        self, data: T, left: Optional[TreeNode[T]] = None, right: Optional[TreeNode[T]] = None
    ) -> None:
        self.data = data
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"({self.data})\n-> {self.left}\n-> {self.right}"
