from __future__ import annotations

from typing import Any, List, Optional


class LinkedListNode:
    def __init__(self, data: int, next_node: Optional[LinkedListNode] = None) -> None:
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        return f"({self.data}) -> {self.next}"


class LinkedList:
    def __init__(self, lst: Optional[LinkedListNode] = None):
        self.head = lst

    @classmethod
    def from_list(cls, lst: List[Any]) -> LinkedList:
        linked_lst = cls()
        for item in lst:
            linked_lst.add(item)
        return linked_lst

    def add(self, data: Any) -> None:
        if self.head is None:
            self.head = LinkedListNode(data)
            return

        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = LinkedListNode(data)

    def remove_last(self) -> Optional[LinkedListNode]:
        """ Deletes the last element of a linked list using only self.head. """

        def _remove_last(lst: Optional[LinkedListNode]) -> Optional[LinkedListNode]:
            if lst is None or lst.next is None:
                return None
            lst.next = _remove_last(lst.next)
            return lst

        return _remove_last(self.head)

    def __repr__(self) -> str:
        return str(self.head)
