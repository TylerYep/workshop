from src.structures import DoublyLinkedList


def test_doubly_linked_list_insert() -> None:
    linked_list = DoublyLinkedList[str]()
    linked_list.insert_at_head("b")
    linked_list.insert_at_tail("c")
    linked_list.insert_at_tail("d")
    linked_list.insert_at_tail("e")
    linked_list.insert_at_head("a")
    assert len(linked_list) == 5
    assert linked_list.pop_tail() == "e"
    assert linked_list.pop_head() == "a"
    assert len(linked_list) == 3
    linked_list.delete("c")
    linked_list.delete("b")
    assert linked_list.pop_head() == "d"
    assert len(linked_list) == 0


def test_print_doubly_linked_list() -> None:
    linked_list = DoublyLinkedList[str]()
    linked_list.insert_at_head("b")
    linked_list.insert_at_tail("c")
    linked_list.insert_at_tail("d")

    assert str(linked_list) == "DoublyLinkedList(head=(b) -> (c) -> (d) -> None)"
