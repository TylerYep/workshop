from typing import TypeVar, cast

import pytest

from cs.structures import BinarySearchTree, RedBlackTree, Tree
from cs.util import Comparable

T = TypeVar("T", bound=Comparable)
parametrize_tree_types = pytest.mark.parametrize(
    "tree_type", ("BinarySearchTree", "RedBlackTree")
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
    @staticmethod
    def test_search(tree_type: str) -> None:
        """ (node.data, node.count, node.frequency) returns: () """
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
    def test_basic_remove(tree_type: str) -> None:
        tree: Tree[int] = construct_tree(tree_type)
        tree.insert(3)
        assert 3 in tree

        tree.remove(3)
        assert 3 not in tree

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
            tree.max_element()
        with pytest.raises(Exception, match="Binary search tree is empty"):
            tree.min_element()
