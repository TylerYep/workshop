import pytest

from cs.structures import LinkedList


class TestLinkedList:
    @staticmethod
    def test_insert() -> None:
        lst = LinkedList[int]()
        assert bool(lst) is False
        for i in range(10):
            lst.insert(i)

        assert bool(lst) is True
        assert len(lst) == 10
        for i in range(10):
            assert i in lst

        assert 13 not in lst
        with pytest.raises(IndexError):
            lst.insert(13, 20)

    @staticmethod
    def test_indexing() -> None:
        lst = LinkedList[int]()
        with pytest.raises(IndexError):
            lst[0] = 5
        with pytest.raises(IndexError):
            _ = lst[0]

        for i in range(10):
            lst.insert(i)

        with pytest.raises(IndexError):
            _ = lst[20]
        with pytest.raises(IndexError):
            lst[20] = 20

        lst[7] = 8
        assert lst[7] == 8

    @staticmethod
    def test_remove() -> None:
        lst = LinkedList[int]()
        with pytest.raises(RuntimeError):
            lst.remove(7)

        for i in range(10):
            lst.add_to_end(i)
        lst.remove(0)
        lst.remove(6)

        for i in range(10):
            lst.insert(i, i // 2)
        lst.remove(6)
        with pytest.raises(RuntimeError):
            lst.remove(6)

    @staticmethod
    def test_remove_last() -> None:
        lst = LinkedList.from_list(list(range(5)))
        assert str(lst) == "LinkedList(head=(0) -> (1) -> (2) -> (3) -> (4) -> None)"
        removed = lst.remove_last()
        assert str(removed) == "(0) -> (1) -> (2) -> (3) -> None"
        removed = lst.remove_last()
        assert str(removed) == "(0) -> (1) -> (2) -> None"

    @staticmethod
    def test_repr() -> None:
        lst = LinkedList[str]()
        lst.insert("A")
        lst.insert("B")

        assert repr(lst) == "LinkedList(head=(B) -> (A) -> None)"
