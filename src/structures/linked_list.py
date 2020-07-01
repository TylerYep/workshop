from __future__ import annotations

from typing import Generic, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class LinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[LinkedListNode[T]] = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[LinkedListNode[T]]:
        node = self.head
        while node is not None:
            yield node
            node = node.next

    @classmethod
    def from_list(cls, lst: List[T]) -> LinkedList[T]:
        linked_lst = cls()
        for item in reversed(lst):
            linked_lst.insert(item)
        return linked_lst

    def insert(self, data: T, index: int = 0) -> None:
        """ Inserts data to the front of the list, or at the specified index. """
        assert index >= 0
        if index == 0:
            self.head = LinkedListNode(data, self.head)
        elif index < self.size:
            curr = self.head
            prev = None
            for _ in range(index):
                prev = curr
                assert curr is not None
                curr = curr.next
            if prev is not None:
                prev.next = LinkedListNode(data, curr)
        self.size += 1

    def search(self, data: T) -> bool:
        curr = self.head
        while curr is not None:
            if curr.data == data:
                return True
            curr = curr.next
        return False

    def remove_node(self, data: T) -> None:
        if self.head is None:
            raise Exception("List is empty")

        if self.head.data == data:
            self.head = self.head.next
            return

        prev = self.head
        for node in self:
            if node.data == data:
                prev.next = node.next
                return
            prev = node

        raise Exception("Node not found")

    def add_to_end(self, data: T) -> None:
        if self.head is None:
            self.head = LinkedListNode(data)
            return

        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = LinkedListNode(data)

    def remove_last(self) -> Optional[LinkedListNode[T]]:
        """ Deletes the last element of a linked list using only self.head. """

        def _remove_last(lst: Optional[LinkedListNode[T]]) -> Optional[LinkedListNode[T]]:
            if lst is None or lst.next is None:
                return None
            lst.next = _remove_last(lst.next)
            return lst

        return _remove_last(self.head)

    def __repr__(self) -> str:
        return str(self.head)


class LinkedListNode(Generic[T]):
    def __init__(self, data: T, next_node: Optional[LinkedListNode[T]] = None) -> None:
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        return f"({self.data}) -> {self.next}"
