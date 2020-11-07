from typing import TypeVar, cast

import pytest

from src.structures import BinarySearchTree, RedBlackTree, Tree
from src.util import Comparable

T = TypeVar("T", bound=Comparable)
TREE_TYPES = ("BinarySearchTree", "RedBlackTree")


def construct_tree(tree_type: str) -> Tree[T]:
    tree_map = {
        constructor.__name__: constructor
        for constructor in (BinarySearchTree, RedBlackTree)
    }
    return cast(Tree[T], tree_map[tree_type]())


class TestTree:
    @staticmethod
    @pytest.mark.parametrize("tree_type", TREE_TYPES)
    def test_search(tree_type: str) -> None:
        t: Tree[int] = construct_tree(tree_type)
        t.insert(6)
        t.insert(13)
        node = t.search(6)
        assert node is not None
        assert node.data == 6

        node = t.search(13)
        assert node is not None
        assert node.data == 13

        assert t.search(2) is None

    @staticmethod
    @pytest.mark.parametrize("tree_type", TREE_TYPES)
    def test_basic_remove(tree_type: str) -> None:
        t: Tree[int] = construct_tree(tree_type)
        t.insert(3)
        assert t.search(3) is not None
        t.remove(3)
        assert t.search(3) is None

    @staticmethod
    @pytest.mark.parametrize("tree_type", TREE_TYPES)
    def test_clear(tree_type: str) -> None:
        t: Tree[int] = construct_tree(tree_type)
        t.clear()
        assert t.root is None
