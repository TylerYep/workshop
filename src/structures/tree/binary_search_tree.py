from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterator, Optional, TypeVar

from dataslots import dataslots

from src.algorithms.sort.comparable import Comparable
from src.util import formatter

T = TypeVar("T", bound=Comparable)


@dataslots
@dataclass(order=True, repr=False)
class TreeNode(Generic[T]):
    data: T
    left: Optional[TreeNode[T]] = None
    right: Optional[TreeNode[T]] = None
    parent: Optional[TreeNode[T]] = field(compare=False, default=None, repr=False)

    def __repr__(self) -> str:
        return str(formatter.pformat(self))

    @property
    def grandparent(self) -> Optional[TreeNode[T]]:
        """ Get the current node's grandparent, or None if it doesn't exist. """
        if self.parent is None:
            return None
        return self.parent.parent

    @property
    def sibling(self) -> Optional[TreeNode[T]]:
        """ Get the current node's sibling, or None if it doesn't exist. """
        if self.parent is None:
            return None
        return self.parent.right if self.parent.left is self else self.parent.left

    def is_root(self) -> bool:
        """ Returns true iff this node is the root of the tree. """
        return self.parent is None

    def is_left(self) -> bool:
        """ Returns true iff this node is the left child of its parent. """
        return self.parent is not None and self.parent.left is self

    def is_right(self) -> bool:
        """ Returns true iff this node is the right child of its parent. """
        return self.parent is not None and self.parent.right is self


@dataclass(init=False)
class BinarySearchTree(Generic[T]):
    """
    We separate the BinarySearchTree with the TreeNode class to allow the root
    of the tree to be None, which allows this implementation to type-check.
    """

    root: Optional[TreeNode[T]]

    def __init__(self) -> None:
        self.root: Optional[TreeNode[T]] = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[TreeNode[T]]:
        node = self.root
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

    def __bool__(self) -> bool:
        return self.root is not None

    def __contains__(self, data: T) -> bool:
        return self.search(data) is not None

    @staticmethod
    def _depth(tree: Optional[TreeNode[T]]) -> int:
        if tree is None:
            return 0
        return 1 + max(
            BinarySearchTree._depth(tree.left), BinarySearchTree._depth(tree.right)
        )

    def clear(self) -> None:
        self.root = None

    def height(self) -> int:
        return self._depth(self.root)

    def is_balanced(self) -> bool:
        if self.root is None:
            raise Exception("Binary search tree is empty")
        return self._depth(self.root.left) == self._depth(self.root.right)

    def search(self, data: T) -> Optional[TreeNode[T]]:
        """ Searches a node in the tree. """

        def _search(node: Optional[TreeNode[T]]) -> Optional[TreeNode[T]]:
            if node is None:
                return None
            if node.data == data:
                return node
            return _search(node.left) if data < node.data else _search(node.right)

        return _search(self.root)

    def insert(self, data: T) -> None:
        """ Puts a new node in the tree. """

        def _insert(
            node: Optional[TreeNode[T]], parent: Optional[TreeNode[T]] = None
        ) -> TreeNode[T]:
            if node is None:
                node = TreeNode(data, parent=parent)
                return node
            if data < node.data:
                node.left = _insert(node.left, node)
            else:
                node.right = _insert(node.right, node)
            return node

        self.root = _insert(self.root)
        self.size += 1

    def remove(self, data: T) -> None:
        """ Removes a node in the tree. """

        def _reassign_nodes(
            node: TreeNode[T], new_children: Optional[TreeNode[T]]
        ) -> None:
            if new_children is not None:
                new_children.parent = node.parent
            if node.parent is not None:
                if node.parent.right == node:
                    node.parent.right = new_children
                else:
                    node.parent.left = new_children
            else:
                self.root = new_children

        def _get_lowest_node(node: TreeNode[T]) -> TreeNode[T]:
            if node.left is not None:
                lowest_node = _get_lowest_node(node.left)
            else:
                lowest_node = node
                _reassign_nodes(node, node.right)
            return lowest_node

        node = self.search(data)
        if node is None:
            raise Exception(f"TreeNode with data {data} does not exist")

        self.size -= 1
        if node.right is None and node.left is None:
            _reassign_nodes(node, None)
        elif node.right is None and node.left is not None:
            _reassign_nodes(node, node.left)
        elif node.right is not None and node.left is None:
            _reassign_nodes(node, node.right)
        elif node.right is not None and node.left is not None:
            lowest_node = _get_lowest_node(node.right)
            lowest_node.left = node.left
            lowest_node.right = node.right
            node.left.parent = lowest_node
            if node.right is not None:
                node.right.parent = lowest_node
            _reassign_nodes(node, lowest_node)

    def max_element(self) -> T:
        """ Gets the max data inserted in the tree. """
        if self.root is None:
            raise Exception("Binary search tree is empty")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.data

    def min_element(self) -> T:
        """ Gets the min data inserted in the tree. """
        if self.root is None:
            raise Exception("Binary search tree is empty")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.data

    def traverse(self, method: str = "inorder") -> Iterator[T]:
        """ Return the pre-order, in-order, or post-order traversal of the tree. """
        if method not in ("preorder", "inorder", "postorder"):
            raise ValueError(
                "Method must be one of: 'preorder', 'inorder', or 'postorder'"
            )

        def _traverse(node: Optional[TreeNode[T]]) -> Iterator[T]:
            if node is not None:
                if method == "preorder":
                    yield node.data
                yield from _traverse(node.left)
                if method == "inorder":
                    yield node.data
                yield from _traverse(node.right)
                if method == "postorder":
                    yield node.data

        return _traverse(self.root)
