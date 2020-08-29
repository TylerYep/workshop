# type: ignore
# pylint: disable=protected-access
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import Generic, Iterator, Optional, TypeVar

from src.algorithms.sort.comparable import Comparable

T = TypeVar("T", bound=Comparable)


@unique
class Color(Enum):
    BLACK = "black"
    RED = "red"


@dataclass
class RedBlackTree(Generic[T]):
    """
    A Red-Black tree, which is a self-balancing BST (binary search
    tree).
    This tree has similar performance to AVL trees, but the balancing is
    less strict, so it will perform faster for writing/deleting nodes
    and slower for reading in the average case, though, because they're
    both balanced binary search trees, both will get the same asymptotic
    performance.
    To read more about them, https://en.wikipedia.org/wiki/Red–black_tree
    Unless otherwise specified, all asymptotic runtimes are specified in
    terms of the size of the tree.
    """

    data: Optional[T] = None
    color: Color = Color.BLACK
    parent: Optional[RedBlackTree[T]] = None
    left: Optional[RedBlackTree[T]] = None
    right: Optional[RedBlackTree[T]] = None

    # Here are functions which are specific to red-black trees

    def rotate_left(self) -> Optional[RedBlackTree[T]]:
        """Rotate the subtree rooted at this node to the left and
        returns the new root to this subtree.
        Performing one rotation can be done in O(1).
        """
        parent = self.parent
        right = self.right
        self.right = right.left
        if self.right:
            self.right.parent = self
        self.parent = right
        right.left = self
        if parent is not None:
            if parent.left == self:
                parent.left = right
            else:
                parent.right = right
        right.parent = parent
        return right

    def rotate_right(self) -> Optional[RedBlackTree[T]]:
        """Rotate the subtree rooted at this node to the right and
        returns the new root to this subtree.
        Performing one rotation can be done in O(1).
        """
        parent = self.parent
        left = self.left
        self.left = left.right
        if self.left:
            self.left.parent = self
        self.parent = left
        left.right = self
        if parent is not None:
            if parent.right is self:
                parent.right = left
            else:
                parent.left = left
        left.parent = parent
        return left

    def insert(self, data: T) -> Optional[RedBlackTree[T]]:
        """Inserts data into the subtree rooted at self, performs any
        rotations necessary to maintain balance, and then returns the
        new root to this subtree (likely self).
        This is guaranteed to run in O(log(n)) time.
        """
        if self.data is None:
            # Only possible with an empty tree
            self.data = data
            return self
        if self.data == data:
            return self
        if self.data > data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = RedBlackTree[T](data, Color.RED, self)
                self.left._insert_repair()
        else:
            if self.right:
                self.right.insert(data)
            else:
                self.right = RedBlackTree[T](data, Color.RED, self)
                self.right._insert_repair()
        return self.parent or self

    def _insert_repair(self) -> None:
        """Repair the coloring from inserting into a tree."""
        if self.parent is None:
            # This node is the root, so it just needs to be black
            self.color = Color.BLACK
        elif color(self.parent) == Color.BLACK:
            # If the parent is black, then it just needs to be red
            self.color = Color.RED
        else:
            uncle = self.parent.sibling
            if color(uncle) == Color.BLACK:
                if self.is_left() and self.parent.is_right():
                    self.parent.rotate_right()
                    self.right._insert_repair()
                elif self.is_right() and self.parent.is_left():
                    self.parent.rotate_left()
                    self.left._insert_repair()
                elif self.is_left():
                    self.grandparent.rotate_right()
                    self.parent.color = Color.BLACK
                    self.parent.right.color = Color.RED
                else:
                    self.grandparent.rotate_left()
                    self.parent.color = Color.BLACK
                    self.parent.left.color = Color.RED
            else:
                self.parent.color = Color.BLACK
                uncle.color = Color.BLACK
                self.grandparent.color = Color.RED
                self.grandparent._insert_repair()

    def remove(self, data) -> Optional[RedBlackTree[T]]:  # pylint: disable=too-many-branches
        """Remove data from this tree."""
        if self.data == data:
            if self.left and self.right:
                # It's easier to balance a node with at most one child,
                # so we replace this node with the greatest one less than
                # it and remove that.
                value = self.left.get_max()
                self.data = value
                self.left.remove(value)
            else:
                # This node has at most one non-None child, so we don't
                # need to replace
                child = self.left or self.right
                if self.color == Color.RED:
                    # This node is red, and its child is black
                    # The only way this happens to a node with one child
                    # is if both children are None leaves.
                    # We can just remove this node and call it a day.
                    if self.is_left():
                        self.parent.left = None
                    else:
                        self.parent.right = None
                else:
                    # The node is black
                    if child is None:
                        # This node and its child are black
                        if self.parent is None:
                            # The tree is now empty
                            return RedBlackTree[T](None)

                        self._remove_repair()
                        if self.is_left():
                            self.parent.left = None
                        else:
                            self.parent.right = None
                        self.parent = None
                    else:
                        # This node is black and its child is red
                        # Move the child node here and make it black
                        self.data = child.data
                        self.left = child.left
                        self.right = child.right
                        if self.left:
                            self.left.parent = self
                        if self.right:
                            self.right.parent = self
        elif self.data > data:
            if self.left:
                self.left.remove(data)
        else:
            if self.right:
                self.right.remove(data)
        return self.parent or self

    def _remove_repair(self) -> None:
        """Repair the coloring of the tree that may have been messed up."""
        if color(self.sibling) == Color.RED:
            self.sibling.color = Color.BLACK
            self.parent.color = Color.RED
            if self.is_left():
                self.parent.rotate_left()
            else:
                self.parent.rotate_right()
        if (
            color(self.parent) == Color.BLACK
            and color(self.sibling) == Color.BLACK
            and color(self.sibling.left) == Color.BLACK
            and color(self.sibling.right) == Color.BLACK
        ):
            self.sibling.color = Color.RED
            self.parent._remove_repair()
            return
        if (
            color(self.parent) == Color.RED
            and color(self.sibling) == Color.BLACK
            and color(self.sibling.left) == Color.BLACK
            and color(self.sibling.right) == Color.BLACK
        ):
            self.sibling.color = Color.RED
            self.parent.color = Color.BLACK
            return
        if (
            self.is_left()
            and color(self.sibling) == Color.BLACK
            and color(self.sibling.right) == Color.BLACK
            and color(self.sibling.left) == Color.RED
        ):
            self.sibling.rotate_right()
            self.sibling.color = Color.BLACK
            self.sibling.right.color = Color.RED
        if (
            self.is_right()
            and color(self.sibling) == Color.BLACK
            and color(self.sibling.right) == Color.RED
            and color(self.sibling.left) == Color.BLACK
        ):
            self.sibling.rotate_left()
            self.sibling.color = Color.BLACK
            self.sibling.left.color = Color.RED
        if (
            self.is_left()
            and color(self.sibling) == Color.BLACK
            and color(self.sibling.right) == Color.RED
        ):
            self.parent.rotate_left()
            self.grandparent.color = self.parent.color
            self.parent.color = Color.BLACK
            self.parent.sibling.color = Color.BLACK
        if (
            self.is_right()
            and color(self.sibling) == Color.BLACK
            and color(self.sibling.left) == Color.RED
        ):
            self.parent.rotate_right()
            self.grandparent.color = self.parent.color
            self.parent.color = Color.BLACK
            self.parent.sibling.color = Color.BLACK

    def check_color_properties(self) -> bool:
        """Check the coloring of the tree, and return True iff the tree
        is colored in a way which matches these five properties:
        (wording stolen from wikipedia article)
         1. Each node is either red or black.
         2. The root node is black.
         3. All leaves are black.
         4. If a node is red, then both its children are black.
         5. Every path from any node to all of its descendent NIL nodes
            has the same number of black nodes.
        This function runs in O(n) time, because properties 4 and 5 take
        that long to check.
        """
        # I assume property 1 to hold because there is nothing that can
        # make the color be anything other than 0 or 1.

        # Property 2
        if self.color == Color.RED:
            # The root was red
            print("Property 2")
            return False

        # Property 3 does not need to be checked, because None is assumed
        # to be black and is all the leaves.

        # Property 4
        if not self.check_coloring():
            print("Property 4")
            return False

        # Property 5
        if self.black_height() is None:
            print("Property 5")
            return False
        # All properties were met
        return True

    def check_coloring(self) -> bool:
        """A helper function to recursively check Property 4 of a
        Red-Black Tree. See check_color_properties for more info.
        """
        if self.color == Color.RED:
            if color(self.left) == Color.RED or color(self.right) == Color.RED:
                return False
        if self.left and not self.left.check_coloring():
            return False
        if self.right and not self.right.check_coloring():
            return False
        return True

    def black_height(self) -> Optional[int]:
        """Returns the number of black nodes from this node to the
        leaves of the tree, or None if there isn't one such value (the
        tree is color incorrectly).
        """
        if self is None:
            # If we're already at a leaf, there is no path
            return 1
        left = RedBlackTree.black_height(self.left)
        right = RedBlackTree.black_height(self.right)
        if left is None or right is None:
            # There are issues with coloring below children nodes
            return None
        if left != right:
            # The two children have unequal depths
            return None
        # Return the black depth of children, plus one if this node is black
        return left + (1 if self.color == Color.BLACK else 0)

    # Here are functions which are general to all binary search trees

    def __contains__(self, data: T) -> bool:
        """Search through the tree for data, returning True iff it is
        found somewhere in the tree.
        Guaranteed to run in O(log(n)) time.
        """
        return self.search(data) is not None

    def search(self, data: T) -> Optional[RedBlackTree[T]]:
        """Search through the tree for data, returning its node if
        it's found, and None otherwise.
        This method is guaranteed to run in O(log(n)) time.
        """
        if self.data == data:
            return self
        if data > self.data:
            if self.right is None:
                return None
            return self.right.search(data)
        if self.left is None:
            return None
        return self.left.search(data)

    def floor(self, data: T) -> Optional[RedBlackTree[T]]:
        """Returns the largest element in this tree which is at most data.
        This method is guaranteed to run in O(log(n)) time."""
        if self.data == data:
            return self.data
        if self.data > data:
            if self.left:
                return self.left.floor(data)
            return None

        if self.right:
            attempt = self.right.floor(data)
            if attempt is not None:
                return attempt
        return self.data

    def ceil(self, data: T) -> Optional[RedBlackTree[T]]:
        """Returns the smallest element in this tree which is at least data.
        This method is guaranteed to run in O(log(n)) time.
        """
        if self.data == data:
            return self.data
        if self.data < data:
            if self.right:
                return self.right.ceil(data)
            return None

        if self.left:
            attempt = self.left.ceil(data)
            if attempt is not None:
                return attempt
        return self.data

    def get_max(self) -> Optional[RedBlackTree[T]]:
        """Returns the largest element in this tree.
        This method is guaranteed to run in O(log(n)) time.
        """
        if self.right:
            # Go as far right as possible
            return self.right.get_max()
        return self.data

    def get_min(self) -> Optional[RedBlackTree[T]]:
        """Returns the smallest element in this tree.
        This method is guaranteed to run in O(log(n)) time.
        """
        if self.left:
            # Go as far left as possible
            return self.left.get_min()
        return self.data

    @property
    def grandparent(self) -> Optional[RedBlackTree[T]]:
        """Get the current node's grandparent, or None if it doesn't exist."""
        if self.parent is None:
            return None
        return self.parent.parent

    @property
    def sibling(self) -> Optional[RedBlackTree[T]]:
        """Get the current node's sibling, or None if it doesn't exist."""
        if self.parent is None:
            return None
        if self.parent.left is self:
            return self.parent.right
        return self.parent.left

    def is_left(self) -> Optional[RedBlackTree[T]]:
        """Returns true iff this node is the left child of its parent."""
        return self.parent and self.parent.left is self

    def is_right(self) -> Optional[RedBlackTree[T]]:
        """Returns true iff this node is the right child of its parent."""
        return self.parent and self.parent.right is self

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        """
        Return the number of nodes in this tree.
        """
        ln = 1
        if self.left:
            ln += len(self.left)
        if self.right:
            ln += len(self.right)
        return ln

    def preorder_traverse(self) -> Iterator[RedBlackTree[T]]:
        yield self.data
        if self.left:
            yield from self.left.preorder_traverse()
        if self.right:
            yield from self.right.preorder_traverse()

    def inorder_traverse(self) -> Iterator[RedBlackTree[T]]:
        if self.left:
            yield from self.left.inorder_traverse()
        yield self.data
        if self.right:
            yield from self.right.inorder_traverse()

    def postorder_traverse(self) -> Iterator[RedBlackTree[T]]:
        if self.left:
            yield from self.left.postorder_traverse()
        if self.right:
            yield from self.right.postorder_traverse()
        yield self.data

    def __repr__(self) -> str:
        from pprint import pformat

        if self.left is None and self.right is None:
            return "'{} {}'".format(self.data, (self.color and "red") or "blk")
        return pformat(
            {"%s %s" % (self.data, (self.color and "red") or "blk"): (self.left, self.right)},
            indent=1,
        )

    def __eq__(self, other: object) -> bool:
        """Test if two trees are equal."""
        if self.data == other.data:
            return self.left == other.left and self.right == other.right
        return False


def color(node: Optional[RedBlackTree[T]]) -> Color:
    """Returns the color of a node, allowing for None leaves."""
    if node is None:
        return Color.BLACK
    return node.color
