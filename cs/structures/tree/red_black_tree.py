from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, unique
from typing import TypeVar

from cs.structures.tree.binary_search_tree import BinarySearchTree, BinaryTreeNode
from cs.util import Comparable, dfield

T = TypeVar("T", bound=Comparable)


@unique
class Color(Enum):
    BLACK = "black"
    RED = "red"


@dataclass(order=True, repr=False, slots=True)
class RedBlackTreeNode(BinaryTreeNode[T]):
    left: RedBlackTreeNode[T] | None = None
    right: RedBlackTreeNode[T] | None = None
    parent: RedBlackTreeNode[T] | None = dfield(None)
    color: Color = dfield(Color.BLACK)
    rank: int = dfield(0)  # Defined here because rank is not updated in BSTs.

    @property
    def grandparent(self) -> RedBlackTreeNode[T] | None:
        """Redefined here because @property cannot be inherited."""
        return None if self.parent is None else self.parent.parent

    @property
    def sibling(self) -> RedBlackTreeNode[T] | None:
        """Redefined here because @property cannot be inherited."""
        if self.parent is None:
            return None
        return self.parent.right if self.parent.left is self else self.parent.left


@dataclass
class RedBlackTree(BinarySearchTree[T]):
    """
    A Red-Black tree, which is a self-balancing BST (binary search tree). This tree has
    similar performance to AVL trees, but the balancing is less strict, so it will
    perform faster for writing/deleting nodes and slower for reading in the average
    case, though, because they're both balanced binary search trees, both will get the
    same asymptotic performance.

    Unless otherwise specified, all asymptotic runtimes are specified in
    terms of the size of the tree.
    """

    root: RedBlackTreeNode[T] | None = None
    size: int = 0

    @staticmethod
    def color(node: RedBlackTreeNode[T] | None) -> Color:
        """Returns the color of a node, allowing for None leaves."""
        return Color.BLACK if node is None else node.color

    @staticmethod
    def opposite_color(node: RedBlackTreeNode[T]) -> Color:
        """Returns the color of a node, allowing for None leaves."""
        return Color.RED if node.color is Color.BLACK else Color.BLACK

    @staticmethod
    def rotate_left(node: RedBlackTreeNode[T]) -> RedBlackTreeNode[T]:
        """
        Rotate the subtree rooted at this node to the left and
        returns the new root to this subtree.
        Performing one rotation can be done in O(1).
        """
        right = node.right
        if right is None:
            raise RuntimeError("There is no left node to rotate to as the new root.")
        node.right = right.left
        if node.right is not None:
            node.right.parent = node
        parent = node.parent
        node.parent = right
        right.left = node
        if parent is not None:
            if node.is_left():
                parent.left = right
            else:
                parent.right = right
        right.parent = parent
        return right

    @staticmethod
    def rotate_right(node: RedBlackTreeNode[T]) -> RedBlackTreeNode[T]:
        """
        Rotate the subtree rooted at this node to the right and
        returns the new root to this subtree.
        Performing one rotation can be done in O(1).
        """
        left = node.left
        if left is None:
            raise RuntimeError("There is no left node to rotate to as the new root.")
        node.left = left.right
        if node.left is not None:
            node.left.parent = node
        parent = node.parent
        node.parent = left
        left.right = node
        if parent is not None:
            if node.is_right():
                parent.right = left
            else:
                parent.left = left
        left.parent = parent
        return left

    def check_correctness(self) -> bool:
        """
        Check the coloring of the tree, and return True iff the tree
        is colored in a way which matches these five properties:
        1. Each node is either red or black.
        2. The root node is black.
        3. All leaves are black.
        4. If a node is red, then both its children are black.
        5. Every path from any node to all of its descendent NIL nodes
            has the same number of black nodes.
        This function runs in O(n) time, because of properties 4 and 5.
        """

        def _check_coloring(node: RedBlackTreeNode[T] | None) -> bool:
            """
            A helper function to recursively check Property 4 of a Red-Black Tree.
            See check_color_properties for more info.
            """
            return node is None or (
                node.color is Color.BLACK
                or self.color(node.left) is self.color(node.right) is Color.BLACK
                and _check_coloring(node.left)
                and _check_coloring(node.right)
            )

        def _black_height(node: RedBlackTreeNode[T] | None) -> int:
            """
            Returns the number of black nodes from this node to the leaves of the tree,
            or -1 if there isn't one such value (the tree is colored incorrectly).
            """
            if node is None:
                return 1
            left = _black_height(node.left)
            right = _black_height(node.right)
            if left != right:
                return -1
            return left + int(node.color is Color.BLACK)

        return self.root is None or (
            self.root.color is Color.BLACK
            and _check_coloring(self.root)
            and _black_height(self.root) != -1
        )

    def insert(self, data: T) -> None:
        """
        Inserts data into the subtree rooted at the root, and then performs any
        rotations necessary to maintain balance.

        This is guaranteed to run in O(log(n)) time.
        """
        self.size += 1
        parent, curr = None, self.root
        while curr is not None:
            parent = curr
            if data == curr.data:
                curr.count += 1
                return
            curr = curr.left if data < curr.data else curr.right

        node = RedBlackTreeNode(data=data, parent=parent)
        if parent is None:
            self.root = node
        elif data < parent.data:
            parent.left = node
        else:
            parent.right = node
        self.insert_repair(node)

    def insert_repair(self, node: RedBlackTreeNode[T]) -> None:
        """Repair the coloring from inserting into a tree."""
        while node.parent is not None:
            # For simplicity, get our parent, sibling, uncle, and grandparent.
            # These are the nodes marked in this diagram:
            #           G
            #          / \
            #         P   A
            #        / \
            #       N   S
            # Here, N is the node itself.
            parent = node.parent
            sibling = node.sibling
            grandparent = node.grandparent
            uncle = parent.sibling

            # If the parent corresponds to a node with one key in the 2-3-4 tree (that
            # is, the parent is a black node), then via the isometry we add ourselves
            # to that node by coloring ourselves red. At that point, we're done.
            # To see if our parent corresponds to a node with one key in the 2-3-4
            # tree, we need to check that
            #   1. the parent is black (if it's red, we're part of a larger node), and
            #   2. the parent has no red children (if it does, then it's part
            #      of a larger node).
            # To do this, we'll find our sibling node (the node across from us under our
            # parent) and confirm that it's not red.

            # If the parent is part of a node with two keys in the 2-3-4 tree, add
            # ourselves to that node. There are several cases to consider here, and
            # they're all symmetric. A node with two keys has one of these shapes,
            # with all possible insertion points marked with an I:
            #          B              B
            #         / \            / \
            #        R   I          I   R
            #       / \                / \
            #      I   I              I   I
            # The commonality is that we would be in one of two cases:
            #    1. We have a black parent and a red sibling.
            #    2. We have a red parent and a black uncle.
            # These two cases function differently. If we're in case 1, we just color
            # ourselves red:
            #         B             B
            #        / \    -->    / \
            #       N   R         R   R
            if self.color(parent) is Color.BLACK and (
                (sibling is None or self.color(sibling) is Color.BLACK)
                or (sibling is not None and self.color(sibling) is Color.RED)
            ):
                node.color = Color.RED
                return

            # There are two subcases here, which correspond to the relative ordering
            # at which the node to insert appears relative to the two other nodes in
            # the 3-node.
            # The first option is the "zig zag" case:
            #       B                   B                   N                B
            #      / \                 / \                 / \              / \
            #     R   B   --->        N   B    --->       R   B    --->    R   R
            #      \     rotate      /        rotate           \  recolor       \
            #       N   N with R    R        N with B           B                B
            # To see whether we're in this case, we have to see whether the orientation
            # of the parent/child and grandparent/parent relations are reversed.
            # The other option is the "zig-zig" case:
            #
            #      B               R                  B
            #     / \             / \                / \
            #    R   B   --->    N   B      --->    R   R
            #   /       rotate        \    recolor       \
            #  N       R with B        B                  B
            if self.color(parent) is Color.RED and (
                uncle is None or self.color(uncle) is Color.BLACK
            ):
                if node.is_left() == parent.is_left():
                    self.rotate_with_parent(parent)
                    parent.color = Color.BLACK
                    node.color = Color.RED
                else:
                    self.rotate_with_parent(node)
                    self.rotate_with_parent(node)
                assert grandparent is not None
                grandparent.color = Color.RED
                return

            # Otherwise, we are inserting into a 4-node. There are several orientations
            # possible here, but with mirroring excluded there are basically two unique
            # insertion points
            #          B              B
            #        /   \          /   \
            #       R     R        R     R
            #      /                \
            #     I                  I
            # We are splitting a node with four keys into a node with two keys, a node
            # with one key, and then kicking one key higher up. This can be done purely
            # by recoloring the nodes and continuing the search from a starred node that
            # is colored black beforehand:
            #          B              B
            #        /   \          /   \
            #       R     R        R     R
            #      /                \
            #     I                  I
            #         vvv            vvvv
            #
            #          #              *
            #        /   \          /   \
            #       B     B        B     B
            #      /                \
            #     R                  R
            # In other words, we just flip the colors of the nodes and propagate the
            # search upward from the grandparent.
            assert uncle is not None
            parent.color = Color.BLACK
            uncle.color = Color.BLACK
            node.color = Color.RED
            node = grandparent  # type: ignore[assignment]

    def rotate_with_parent(self, node: RedBlackTreeNode[T]) -> None:
        """
        Rotate the subtree rooted at this node to the right and
        returns the new root to this subtree.
        Performing one rotation can be done in O(1).
        """
        if node.parent is None:
            raise RuntimeError("Node is the root and has no parent.")

        # Step 1: Do the logic to "locally" rotate the nodes. This repositions the
        # node, its parent, and the middle child. However, it leaves the parent
        # pointers of these nodes unmodified; we'll handle that later.
        child = None
        if node.is_left():
            # Rotate right
            child = node.right
            node.right = node.parent
            node.parent.left = child
            node.parent.rank = node.parent.rank - node.rank - 1
        else:
            # Rotate left
            child = node.left
            node.left = node.parent
            node.parent.right = child
            node.rank = node.parent.rank + node.rank + 1

        # Step 2: Make the node's grandparent now point at it.
        grandparent = node.grandparent
        if grandparent is None:
            self.root = node
        else:
            if node.parent.is_left():
                grandparent.left = node
            else:
                grandparent.right = node

        # Step 3: Update parent pointers.
        #  1. The child node that got swapped needs its parent updated.
        #  2. The node we rotated now has a new parent.
        #  3. The node's old parent now points to the node we rotated.
        # We have to be super careful about this, though, because some of these
        # nodes might not exist and we need to not lose any pointers.
        if child is not None:
            child.parent = node.parent
        old_parent = node.parent
        node.parent = old_parent.parent
        old_parent.parent = node

    def select(self, rank: int) -> T:
        """Takes in an integer rank and returns the rank-th order statistic."""
        curr = self.root
        while curr is not None:
            if rank == curr.rank:
                return curr.data
            if rank < curr.rank:
                curr = curr.left
            else:
                rank -= curr.rank + 1
                curr = curr.right
        raise RuntimeError("Not enough elements in tree.")

    def rank_of(self, data: T) -> int:
        """
        Inverse of select; takes in a node in the tree and returns the number
        of elements in the tree smaller than that key.
        """
        curr = self.root
        total = 0
        while curr is not None:
            if data == curr.data:
                return total + curr.rank
            if data < curr.data:
                curr = curr.left
            else:
                total += curr.rank + 1
                curr = curr.right
        return total

    # TODO: fix remove()
    # def remove(self, data: T) -> None:
    #     def _remove(node: RedBlackTreeNode[T]) -> RedBlackTreeNode[T] | None:
    #         nonlocal data
    #         if node.data == data:
    #             if node.left is not None and node.right is not None:
    #                 # It's easier to balance a node with at most one child,
    #                 # so we replace this node with the greatest one less than
    #                 # it and remove that.
    #                 value = node.left.get_max()
    #                 node.data = value
    #                 data = value
    #                 _remove(node.left)
    #             else:
    #                 # This node has at most one non-None child, so we don't
    #                 # need to replace
    #                 child = node.left or node.right
    #                 if node.color is Color.RED:
    #                     # This node is red, and its child is black
    #                     # The only way this happens to a node with one child
    #                     # is if both children are None leaves.
    #                     # We can just remove this node and call it a day.
    #                     if node.is_left():
    #                         node.parent.left = None
    #                     else:
    #                         node.parent.right = None
    #                 else:
    #                     # The node is black
    #                     if child is None:
    #                         # This node and its child are black
    #                         if node.parent is None:
    #                             # The tree is now empty
    #                             return

    #                         self._remove_repair(node)
    #                         if node.is_left:
    #                             node.parent.left = None
    #                         else:
    #                             node.parent.right = None
    #                         node.parent = None
    #                     else:
    #                         # This node is black and its child is red
    #                         # Move the child node here and make it black
    #                         node.data = child.data
    #                         node.left = child.left
    #                         node.right = child.right
    #                         if node.left:
    #                             node.left.parent = self.root
    #                         if node.right:
    #                             node.right.parent = self.root
    #         elif node.data > data:
    #             if node.left:
    #                 _remove(node.left)
    #         else:
    #             if node.right:
    #                 _remove(node.right)

    #     _remove(self.root)

    # def _remove_repair(self, node: RedBlackTreeNode[T]) -> None:
    #         #  if self.color(node.sibling) is Color.RED:
    #         node.sibling.color = Color.BLACK
    #         node.parent.color = Color.RED
    #         if node.is_left:
    #             self.rotate_left(node.parent)
    #         else:
    #             self.rotate_right(node.parent)
    #     if (
    #         self.color(node.parent) is Color.BLACK
    #         and self.color(node.sibling) is Color.BLACK
    #         and self.color(node.sibling.left) is Color.BLACK
    #         and self.color(node.sibling.right) is Color.BLACK
    #     ):
    #         node.sibling.color = Color.RED
    #         self._remove_repair(node.parent)
    #         return
    #     if (
    #         self.color(node.parent) is Color.RED
    #         and self.color(node.sibling) is Color.BLACK
    #         and self.color(node.sibling.left) is Color.BLACK
    #         and self.color(node.sibling.right) is Color.BLACK
    #     ):
    #         node.sibling.color = Color.RED
    #         node.parent.color = Color.BLACK
    #         return
    #     if (
    #         node.is_left
    #         and self.color(node.sibling) is Color.BLACK
    #         and self.color(node.sibling.right) is Color.BLACK
    #         and self.color(node.sibling.left) is Color.RED
    #     ):
    #         self.rotate_right(node.sibling)
    #         node.sibling.color = Color.BLACK
    #         node.sibling.right.color = Color.RED
    #     if (
    #         node.is_right
    #         and self.color(node.sibling) is Color.BLACK
    #         and self.color(node.sibling.right) is Color.RED
    #         and self.color(node.sibling.left) is Color.BLACK
    #     ):
    #         self.rotate_left(node.sibling)
    #         node.sibling.color = Color.BLACK
    #         node.sibling.left.color = Color.RED
    #     if (
    #         node.is_left
    #         and self.color(node.sibling) is Color.BLACK
    #         and self.color(node.sibling.right) is Color.RED
    #     ):
    #         self.rotate_left(node.parent)
    #         node.grandparent.color = node.parent.color
    #         node.parent.color = Color.BLACK
    #         node.parent.sibling.color = Color.BLACK
    #     if (
    #         node.is_right
    #         and self.color(node.sibling) is Color.BLACK
    #         and self.color(node.sibling.left) is Color.RED
    #     ):
    #         self.rotate_right(node.parent)
    #         node.grandparent.color = node.parent.color
    #         node.parent.color = Color.BLACK
    #         node.parent.sibling.color = Color.BLACK
