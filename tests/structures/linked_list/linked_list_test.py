from src.structures import LinkedList


class TestLinkedList:
    @staticmethod
    def test_insert() -> None:
        lst = LinkedList[int]()
        for i in range(10):
            lst.insert(i)

        assert len(lst) == 10
        for i in range(10):
            assert i in lst

    @staticmethod
    def test_remove_last() -> None:
        lst = LinkedList.from_list(list(range(5)))
        assert str(lst) == "LinkedList(head=(0) -> (1) -> (2) -> (3) -> (4) -> None)"
        removed = lst.remove_last()
        assert str(removed) == "(0) -> (1) -> (2) -> (3) -> None"
        removed = lst.remove_last()
        assert str(removed) == "(0) -> (1) -> (2) -> None"
