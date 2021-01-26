from __future__ import annotations

from conftest import assert_a_faster_than_b
from cs.structures import DisjointSet


class TestDisjointSet:
    @staticmethod
    def test_make_set() -> None:
        dset: DisjointSet[int | str] = DisjointSet()
        assert not dset
        assert 1 not in dset
        for i in range(5):
            dset.make_set(i)
            dset.make_set(str(i))
        assert dset
        assert 1 in dset
        dset.make_set(1)

    @staticmethod
    def test_find_set() -> None:
        dset = DisjointSet[int]()
        for i in range(10):
            dset.make_set(i)
        for i in range(10):
            assert dset.find_set(i) == i

    @staticmethod
    def test_union_set() -> None:
        dset = DisjointSet[int]()
        for i in range(5):
            dset.make_set(i)
        dset.union(0, 2)
        dset.union(4, 2)
        dset.union(3, 1)
        assert dset.is_connected(4, 0) is True
        assert dset.is_connected(1, 0) is False
        assert dset.itersets() == [{0, 2, 4}, {1, 3}]

    @staticmethod
    def test_optimization() -> None:
        dset = DisjointSet[int]()
        for i in range(500):
            dset.make_set(i)
        for i in range(1, 480):
            dset.union(i, i + 4)

        assert_a_faster_than_b(dset.itersets, dset.naive_itersets)

    @staticmethod
    def test_print_disjoint_set() -> None:
        dset = DisjointSet[int]()
        for i in range(7):
            dset.make_set(i)
        dset.union(0, 2)
        dset.union(5, 2)
        dset.union(3, 1)

        assert repr(dset) == str(dset) == "DisjointSet([{0, 2, 5}, {1, 3}, {4}, {6}])"

    @staticmethod
    def test_unites_symmetrically() -> None:
        dset = DisjointSet[int]()
        for i in range(10):
            dset.make_set(i)
        dset.union(1, 2)
        dset.union(3, 4)
        dset.union(1, 6)
        dset.union(8, 2)

        assert dset.is_connected(6, 8) is True
        assert dset.is_connected(8, 6) is True
