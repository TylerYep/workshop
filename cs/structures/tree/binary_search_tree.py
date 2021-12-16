from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TypeVar

from cs.structures.tree.tree import Tree, TreeNode
from cs.util import Comparable, dfield

T = TypeVar("T", bound=Comparable)


@dataclass(order=True, repr=False, slots=True)
class BinaryTreeNode(TreeNode[T]):
    left: BinaryTreeNode[T] | None = None
    right: BinaryTreeNode[T] | None = None
    parent: BinaryTreeNode[T] | None = dfield(None)

    @property
    def grandparent(self) -> BinaryTreeNode[T] | None:
        """Get the current node's grandparent, or None if it doesn't exist."""
        return None if self.parent is None else self.parent.parent

    @property
    def sibling(self) -> BinaryTreeNode[T] | None:
        """Get the current node's sibling, or None if it doesn't exist."""
        if self.parent is None:
            return None
        return self.parent.right if self.parent.left is self else self.parent.left

    def is_root(self) -> bool:
        """Returns true iff this node is the root of the tree."""
        return self.parent is None

    def is_left(self) -> bool:
        """Returns true iff this node is the left child of its parent."""
        return self.parent is not None and self.parent.left is self

    def is_right(self) -> bool:
        """Returns true iff this node is the right child of its parent."""
        return self.parent is not None and self.parent.right is self


@dataclass
class BinarySearchTree(Tree[T]):
    """
    BinarySearchTrees contain nodes in sorted order.

    We separate the BinarySearchTree with the TreeNode class to allow the root
    of the tree to be None, which allows this implementation to type-check.
    """

    root: BinaryTreeNode[T] | None = None
    size: int = 0

    def __iter__(self) -> Iterator[BinaryTreeNode[T]]:
        """Performs an in-order traversal over the TreeNodes of the Tree."""

        def _iter(node: BinaryTreeNode[T] | None) -> Iterator[BinaryTreeNode[T]]:
            if node is not None:
                yield from _iter(node.left)
                yield node
                yield from _iter(node.right)

        return _iter(self.root)

    def __str__(self) -> str:
        from cs.structures.tree.draw_tree import draw_tree

        return draw_tree(self.root)

    @staticmethod
    def depth(tree: BinaryTreeNode[T] | None) -> int:
        if tree is None:
            return 0
        return 1 + max(
            BinarySearchTree.depth(tree.left), BinarySearchTree.depth(tree.right)
        )

    def height(self) -> int:
        return self.depth(self.root)

    def is_balanced(self) -> bool:
        if self.root is None:
            raise Exception("Binary search tree is empty")
        return self.depth(self.root.left) == self.depth(self.root.right)

    def search(self, data: T) -> BinaryTreeNode[T] | None:
        """Searches a node in the tree."""

        def _search(node: BinaryTreeNode[T] | None) -> BinaryTreeNode[T] | None:
            if node is None:
                return None
            if node.data == data:
                node.hits += 1
                return node
            return _search(node.left) if data < node.data else _search(node.right)

        return _search(self.root)

    def insert(self, data: T) -> None:
        """Puts a new node in the tree."""

        def _insert(
            node: BinaryTreeNode[T] | None, parent: BinaryTreeNode[T] | None = None
        ) -> BinaryTreeNode[T]:
            if node is None:
                node = BinaryTreeNode(data, parent=parent)
                return node
            if data == node.data:
                node.count += 1
            elif data < node.data:
                node.left = _insert(node.left, node)
            else:
                node.right = _insert(node.right, node)
            return node

        self.root = _insert(self.root)
        self.size += 1

    def remove(self, data: T) -> None:
        """Removes a node in the tree."""

        def _reassign_nodes(
            node: BinaryTreeNode[T], new_child: BinaryTreeNode[T] | None
        ) -> None:
            if new_child is not None:
                new_child.parent = node.parent

            if node.parent is None:
                self.root = new_child
            elif node.parent.right == node:
                node.parent.right = new_child
            else:
                node.parent.left = new_child

        def _get_lowest_node(node: BinaryTreeNode[T]) -> BinaryTreeNode[T]:
            if node.left is None:
                lowest_node = node
                _reassign_nodes(node, node.right)
            else:
                lowest_node = _get_lowest_node(node.left)
            return lowest_node

        node = self.search(data)
        if node is None:
            raise Exception(f"TreeNode with data {data} does not exist")
        self.size -= 1

        # If count is greater than 1, we just decrease the count and return. We reduce
        # the node count regardless in case we are holding a reference to the node.
        node.count -= 1
        if node.count > 0:
            return
        if node.right is None:
            _reassign_nodes(node, node.left)
        elif node.left is None:
            _reassign_nodes(node, node.right)
        else:
            lowest_node = _get_lowest_node(node.right)
            lowest_node.left = node.left
            lowest_node.right = node.right
            if node.left is not None:
                node.left.parent = lowest_node
            if node.right is not None:
                node.right.parent = lowest_node
            _reassign_nodes(node, lowest_node)

    def max_element(self) -> T:
        """Gets the max data inserted in the tree."""
        if self.root is None:
            raise Exception("Binary search tree is empty")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.data

    def min_element(self) -> T:
        """Gets the min data inserted in the tree."""
        if self.root is None:
            raise Exception("Binary search tree is empty")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.data

    def traverse(self, method: str = "inorder") -> Iterator[T]:
        """Return the pre-order, in-order, or post-order traversal of the tree."""
        if method not in ("preorder", "inorder", "postorder"):
            raise ValueError(
                "Method must be one of: 'preorder', 'inorder', or 'postorder'"
            )

        def _traverse(node: BinaryTreeNode[T] | None) -> Iterator[T]:
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

    def select(self, rank: int) -> T:
        """
        Takes in an integer rank and returns the rank-th order statistic.

        (Equivalent code, but this solution avoids evaluating the iterator)
            return list(self)[rank].data
        """
        return next(node for i, node in enumerate(self) if i == rank).data

    def rank_of(self, data: T) -> int:
        return next(i for i, node in enumerate(self) if node.data == data)
