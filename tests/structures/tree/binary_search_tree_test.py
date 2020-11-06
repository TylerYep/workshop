import pytest

from src.structures import BinarySearchTree


class TestBinarySearchTree:
    @staticmethod
    @pytest.fixture
    def t() -> BinarySearchTree[int]:
        r"""
        8
        / \
        3   10
        / \    \
        1   6    14
            / \   /
            4   7 13
            \
            5
        """
        tree = BinarySearchTree[int]()
        tree.insert(8)
        tree.insert(3)
        tree.insert(6)
        tree.insert(1)
        tree.insert(10)
        tree.insert(14)
        tree.insert(13)
        tree.insert(4)
        tree.insert(7)
        tree.insert(5)
        return tree

    @staticmethod
    def test_insert() -> None:
        t = BinarySearchTree[int]()
        assert len(t) == 0

        t.insert(8)
        assert t.root is not None

        assert t.root.parent is None
        assert t.root.data == 8

        t.insert(10)
        r"""
              8
               \
                10
        """
        assert t.root.right is not None

        assert t.root.right.parent == t.root
        assert t.root.right.data == 10

        t.insert(3)
        r"""
              8
             / \
            3   10
        """
        assert t.root.left is not None

        assert t.root.left.parent == t.root
        assert t.root.left.data == 3

        t.insert(6)
        r"""
              8
             / \
            3   10
             \
              6
        """
        assert t.root.left.right is not None

        assert t.root.left.right.parent == t.root.left
        assert t.root.left.right.data == 6

        t.insert(1)
        r"""
              8
             / \
            3   10
           / \
          1   6
        """
        assert t.root.left.left is not None

        assert t.root.left.left.parent == t.root.left
        assert t.root.left.left.data == 1

    @staticmethod
    def test_search(t: BinarySearchTree[int]) -> None:
        node = t.search(6)
        assert node is not None
        assert node.data == 6

        node = t.search(13)
        assert node is not None
        assert node.data == 13

        assert t.search(2) is None

    @staticmethod
    def test_basic_remove() -> None:
        t = BinarySearchTree[int]()
        t.insert(3)
        assert t.search(3) is not None
        t.remove(3)
        assert t.search(3) is None

    @staticmethod
    def test_remove(t: BinarySearchTree[int]) -> None:

        t.remove(13)
        r"""
              8
             / \
            3   10
           / \    \
          1   6    14
             / \
            4   7
             \
              5
        """
        assert t.root is not None
        assert t.root.right is not None
        assert t.root.left is not None
        assert t.root.left.left is not None
        assert t.root.left.right is not None
        assert t.root.left.right.right is not None
        assert t.root.right.right is not None
        assert t.root.left.right is not None

        assert t.root.right.right.right is None
        assert t.root.right.right.left is None

        t.remove(7)
        r"""
              8
             / \
            3   10
           / \    \
          1   6    14
             /
            4
             \
              5
        """
        assert t.root.left.right.right is None
        assert t.root.left.right.left.data == 4

        t.remove(6)
        r"""
              8
             / \
            3   10
           / \    \
          1   4    14
               \
                5
        """
        assert t.root.left.left.data == 1
        assert t.root.left.right.data == 4
        assert t.root.left.right.right.data == 5
        assert t.root.left.right.left is None
        assert t.root.left.left.parent == t.root.left
        assert t.root.left.right.parent == t.root.left

        t.remove(3)
        r"""
              8
             / \
            4   10
           / \    \
          1   5    14
        """

        assert t.root.left.data == 4
        assert t.root.left.right.data == 5
        assert t.root.left.left.data == 1
        assert t.root.left.parent == t.root
        assert t.root.left.left.parent == t.root.left
        assert t.root.left.right.parent == t.root.left

        t.remove(4)
        r"""
              8
             / \
            5   10
           /      \
          1        14
        """
        assert t.root.left.data == 5
        assert t.root.left.right is None
        assert t.root.left.left.data == 1
        assert t.root.left.parent == t.root
        assert t.root.left.left.parent == t.root.left

        with pytest.raises(Exception):
            t.remove(42)

        t.remove(8)
        t.remove(1)
        t.remove(10)
        t.remove(14)
        t.remove(5)
        assert t.root is None

    @staticmethod
    def test_remove_2(t: BinarySearchTree[int]) -> None:
        t.remove(3)
        r"""
              8
             / \
            4   10
           / \    \
          1   6    14
             / \   /
            5   7 13
        """
        assert t.root is not None
        assert t.root.left is not None
        assert t.root.left.left is not None
        assert t.root.left.right is not None
        assert t.root.left.right.left is not None
        assert t.root.left.right.right is not None

        assert t.root.left.data == 4
        assert t.root.left.right.data == 6
        assert t.root.left.left.data == 1
        assert t.root.left.right.right.data == 7
        assert t.root.left.right.left.data == 5
        assert t.root.left.parent == t.root
        assert t.root.left.right.parent == t.root.left
        assert t.root.left.left.parent == t.root.left
        assert t.root.left.right.left.parent == t.root.left.right

    @staticmethod
    def test_clear(t: BinarySearchTree[int]) -> None:
        t.clear()
        assert t.root is None

    @staticmethod
    def test_contains(t: BinarySearchTree[int]) -> None:
        assert 6 in t
        assert -1 not in t

    @staticmethod
    def test_get_max_data(t: BinarySearchTree[int]) -> None:
        assert t.max_element() == 14

        t.clear()
        with pytest.raises(Exception):
            t.max_element()

    @staticmethod
    def test_get_min_data(t: BinarySearchTree[int]) -> None:
        assert t.min_element() == 1

        t.clear()
        with pytest.raises(Exception):
            t.min_element()

    @staticmethod
    def test_inorder_traversal(t: BinarySearchTree[int]) -> None:
        expected = [1, 3, 4, 5, 6, 7, 8, 10, 13, 14]
        assert list(t.traverse("inorder")) == expected

    @staticmethod
    def test_preorder_traversal(t: BinarySearchTree[int]) -> None:
        expected = [8, 3, 1, 6, 4, 5, 7, 10, 14, 13]
        assert list(t.traverse("preorder")) == expected

    @staticmethod
    def test_print_tree() -> None:
        tree = BinarySearchTree[int]()
        tree.insert(8)
        tree.insert(6)
        tree.insert(1)
        tree.insert(73)
        tree.insert(11)

        assert (
            repr(tree)
            == str(tree)
            == (
                "BinarySearchTree(root=BinaryTreeNode(\n"
                "    data=8,\n"
                "    left=BinaryTreeNode(data=6, left=BinaryTreeNode(data=1)),\n"
                "    right=BinaryTreeNode(data=73, left=BinaryTreeNode(data=11))\n"
                "), size=5)"
            )
        )
