from typing import TYPE_CHECKING, TypeVar, cast

import pytest

from cs.structures import BinarySearchTree, RedBlackTree, Tree
from cs.util import Comparable

if TYPE_CHECKING:
    from cs.structures.tree.tree import TreeNode

T = TypeVar("T", bound=Comparable)
parametrize_tree_types = pytest.mark.parametrize(
    "tree_type", ["BinarySearchTree", "RedBlackTree"]
)
TEN_ELEMS = (8, 3, 6, 1, 10, 14, 13, 4, 7, 5)


def construct_tree(tree_type: str) -> Tree[T]:
    tree_map = {
        constructor.__name__: constructor
        for constructor in (BinarySearchTree, RedBlackTree)
    }
    return cast(Tree[T], tree_map[tree_type]())


@parametrize_tree_types
class TestTree:
    """Tests all types of trees. Note that trees are not necessarily sorted BSTs."""

    @staticmethod
    def test_iter(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        for elem in TEN_ELEMS:
            tree.insert(elem)

        prev: TreeNode[int] | None = None
        for node in tree:
            assert prev is None or prev.data < node.data
            prev = node

    @staticmethod
    def test_height_is_balanced(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        for elem in (50, 25, 75, 0, 100):
            tree.insert(elem)

        assert tree.is_balanced() is True
        assert tree.height() == 3

    @staticmethod
    def test_search(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        for i in (6, 13, 7, 1, 9):
            tree.insert(i)

        assert tree.search(2) is None

        node = tree.search(6)
        assert node is not None
        assert (node.data, node.count, node.hits) == (6, 1, 1)

        node = tree.search(13)
        assert node is not None
        assert (node.data, node.count, node.hits) == (13, 1, 1)

        tree.insert(6)
        node = tree.search(6)
        assert node is not None
        assert (node.data, node.count, node.hits) == (6, 2, 2)

    @staticmethod
    def test_contains(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        for elem in (0, 8, -8, 4, 12, 10, 11):
            tree.insert(elem)

        for elem in (5, -6, -10, 13):
            assert elem not in tree
        for elem in (11, 12, -8, 0):
            assert elem in tree

    @staticmethod
    def test_basic_remove(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        tree.insert(3)
        assert 3 in tree

        node = tree.search(3)
        tree.insert(3)
        assert node is not None
        assert node.count == 2
        tree.remove(3)
        assert node.count == 1

        tree.remove(3)
        assert 3 not in tree
        assert node.count == 0

    @staticmethod
    def test_clear(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        tree.clear()
        assert tree.root is None

    @staticmethod
    def test_get_max_min(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        for i in TEN_ELEMS:
            tree.insert(i)
        assert tree.max_element() == 14
        assert tree.min_element() == 1

        tree.clear()
        with pytest.raises(Exception, match="Binary search tree is empty"):
            _ = tree.max_element()
        with pytest.raises(Exception, match="Binary search tree is empty"):
            _ = tree.min_element()

    @staticmethod
    def test_rank_select(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        for elem in TEN_ELEMS:
            tree.insert(elem)

        if isinstance(tree, RedBlackTree):
            return  # TODO: fix RedBlackTrees

        # [1, 3, 4, 5, 6, 7, 8, 10, 13, 14]
        assert tree.select(7) == 10
        assert tree.select(9) == 14

        assert 5 in tree
        assert tree.rank_of(5) == 3
        assert 10 in tree
        assert tree.rank_of(10) == 7
