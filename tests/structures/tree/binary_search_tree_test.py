import pytest

from cs.structures import BinarySearchTree
from tests.structures.tree.tree_test import TEN_ELEMS


class TestBinarySearchTree:
    @staticmethod
    @pytest.fixture
    def tree() -> BinarySearchTree[int]:
        tree = BinarySearchTree[int]()
        for elem in TEN_ELEMS:
            tree.insert(elem)
        return tree

    @staticmethod
    def test_tree_traversal(tree: BinarySearchTree[int]) -> None:
        assert list(tree.traverse("preorder")) == [8, 3, 1, 6, 4, 5, 7, 10, 14, 13]
        assert list(tree.traverse("inorder")) == [1, 3, 4, 5, 6, 7, 8, 10, 13, 14]
        assert list(tree.traverse("postorder")) == [1, 5, 4, 7, 6, 3, 13, 14, 10, 8]

    @staticmethod
    def test_tree_repr() -> None:
        tree = BinarySearchTree[int]()
        for i in (8, 6, 1, 73, 11):
            tree.insert(i)

        assert repr(tree) == (
            "BinarySearchTree(root=BinaryTreeNode(\n"
            "    data=8,\n"
            "    left=BinaryTreeNode(data=6, left=BinaryTreeNode(data=1)),\n"
            "    right=BinaryTreeNode(data=73, left=BinaryTreeNode(data=11))\n"
            "), size=5)"
        )

    @staticmethod
    def test_insert() -> None:
        tree = BinarySearchTree[int]()
        assert not tree

        tree.insert(8)

        assert tree.root is not None
        assert tree.root.parent is None
        assert tree.root.data == 8

        tree.insert(10)

        assert str(tree).split("\n") == [
            "8",
            " \\",
            " 10",
            "",
        ]
        assert tree.root.right is not None
        assert tree.root.right.parent == tree.root
        assert tree.root.right.data == 10

        tree.insert(3)

        assert str(tree).split("\n") == [
            "  8",
            " / \\",
            "3  10",
            "",
        ]
        assert tree.root.left is not None
        assert tree.root.left.parent == tree.root
        assert tree.root.left.data == 3

        tree.insert(6)

        assert str(tree).split("\n") == [
            "  8",
            " / \\",
            "3  10",
            " \\",
            "  6",
            "",
        ]
        assert tree.root.left.right is not None
        assert tree.root.left.right.parent == tree.root.left
        assert tree.root.left.right.data == 6

        tree.insert(1)

        assert str(tree).split("\n") == [
            "    8",
            "   / \\",
            "  3  10",
            " / \\",
            "1   6",
            "",
        ]
        assert tree.root.left.left is not None
        assert tree.root.left.left.parent == tree.root.left
        assert tree.root.left.left.data == 1
        assert len(tree) == 5

    @staticmethod
    def test_remove(tree: BinarySearchTree[int]) -> None:
        tree.remove(13)

        assert str(tree).split("\n") == [
            "     8",
            "    / \\",
            "   /   \\",
            "  3    10",
            " / \\     \\",
            "1   6    14",
            "   / \\",
            "  4   7",
            "   \\",
            "    5",
            "",
        ]
        assert tree.root is not None
        assert tree.root.right is not None
        assert tree.root.left is not None
        assert tree.root.left.left is not None
        assert tree.root.left.right is not None
        assert tree.root.left.right.right is not None
        assert tree.root.right.right is not None
        assert tree.root.left.right is not None

        assert tree.root.right.right.right is None
        assert tree.root.right.right.left is None

        tree.remove(7)

        assert str(tree).split("\n") == [
            "     8",
            "    / \\",
            "   /   \\",
            "  3    10",
            " / \\     \\",
            "1   6    14",
            "   /",
            "  /",
            " 4",
            "  \\",
            "   5",
            "",
        ]
        assert tree.root.left.right.right is None
        assert tree.root.left.right.left.data == 4

        tree.remove(6)

        assert str(tree).split("\n") == [
            "     8",
            "    / \\",
            "   /   \\",
            "  3    10",
            " / \\     \\",
            "1   4    14",
            "     \\",
            "      5",
            "",
        ]
        assert tree.root.left.left.data == 1
        assert tree.root.left.right.data == 4
        assert tree.root.left.right.right.data == 5
        assert tree.root.left.right.left is None
        assert tree.root.left.left.parent == tree.root.left
        assert tree.root.left.right.parent == tree.root.left

        tree.remove(3)

        assert str(tree).split("\n") == [
            "     8",
            "    / \\",
            "   /   \\",
            "  4    10",
            " / \\     \\",
            "1   5    14",
            "",
        ]
        assert tree.root.left.data == 4
        assert tree.root.left.right.data == 5
        assert tree.root.left.left.data == 1
        assert tree.root.left.parent == tree.root
        assert tree.root.left.left.parent == tree.root.left
        assert tree.root.left.right.parent == tree.root.left

        tree.remove(4)

        assert str(tree).split("\n") == [
            "     8",
            "    / \\",
            "   /   \\",
            "  5    10",
            " /       \\",
            "1        14",
            "",
        ]
        assert tree.root.left.data == 5
        assert tree.root.left.right is None
        assert tree.root.left.left.data == 1
        assert tree.root.left.parent == tree.root
        assert tree.root.left.left.parent == tree.root.left

        with pytest.raises(Exception, match="TreeNode with data 42 does not exist"):
            tree.remove(42)

        for elem in (8, 1, 10, 14, 5):
            tree.remove(elem)

        assert tree.root is None
        assert str(tree).split("\n") == [""]

    @staticmethod
    def test_remove_2(tree: BinarySearchTree[int]) -> None:
        tree.remove(3)

        assert str(tree).split("\n") == [
            "      8",
            "     / \\",
            "    /   \\",
            "   /     \\",
            "  4      10",
            " / \\       \\",
            "1   6      14",
            "   / \\     /",
            "  5   7   13",
            "",
        ]
        assert tree.root is not None
        assert tree.root.left is not None
        assert tree.root.left.left is not None
        assert tree.root.left.right is not None
        assert tree.root.left.right.left is not None
        assert tree.root.left.right.right is not None

        assert tree.root.left.data == 4
        assert tree.root.left.right.data == 6
        assert tree.root.left.left.data == 1
        assert tree.root.left.right.right.data == 7
        assert tree.root.left.right.left.data == 5
        assert tree.root.left.parent == tree.root
        assert tree.root.left.right.parent == tree.root.left
        assert tree.root.left.left.parent == tree.root.left
        assert tree.root.left.right.left.parent == tree.root.left.right
