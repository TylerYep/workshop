from src.structures.linked_list import LinkedList


def test_remove_last() -> None:
    lst = LinkedList.from_list(list(range(5)))
    assert str(lst) == "(0) -> (1) -> (2) -> (3) -> (4) -> None"
    removed = lst.remove_last()
    assert str(removed) == "(0) -> (1) -> (2) -> (3) -> None"
    removed = lst.remove_last()
    assert str(removed) == "(0) -> (1) -> (2) -> None"
