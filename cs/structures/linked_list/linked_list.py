from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(repr=False, slots=True)
class LinkedListNode(Generic[T]):
    data: T
    next: LinkedListNode[T] | None = None

    def __repr__(self) -> str:
        return f"({self.data}) -> {self.next}"


@dataclass(init=False)
class LinkedList(Generic[T]):
    head: LinkedListNode[T] | None

    def __init__(self) -> None:
        self.head = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[LinkedListNode[T]]:
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __bool__(self) -> bool:
        return self.head is not None

    def __contains__(self, item: T) -> bool:
        curr = self.head
        while curr is not None:
            if curr.data == item:
                return True
            curr = curr.next
        return False

    def __getitem__(self, index: int) -> T:
        current = self.head
        if current is None:
            raise IndexError("List is empty")
        for _ in range(index):
            if current.next is None:
                raise IndexError("Index out of range.")
            current = current.next
        return current.data

    def __setitem__(self, index: int, data: T) -> None:
        current = self.head
        if current is None:
            raise IndexError("List is empty")
        for _ in range(index):
            if current.next is None:
                raise IndexError("Index out of range.")
            current = current.next
        current.data = data

    @classmethod
    def from_list(cls, lst: list[T]) -> LinkedList[T]:
        linked_lst = cls()
        for item in reversed(lst):
            linked_lst.insert(item)
        return linked_lst

    def insert(self, data: T, index: int = 0) -> None:
        """Inserts data to the front of the list, or at the specified index."""
        if index < 0 or index > self.size:
            raise IndexError
        self.size += 1
        if index == 0:
            self.head = LinkedListNode(data, self.head)
            return

        curr = self.head
        prev = None
        for _ in range(index):
            prev = curr
            if curr is None:
                raise ValueError
            curr = curr.next
        if prev is not None:
            prev.next = LinkedListNode(data, curr)

    def remove(self, data: T) -> None:
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

    def remove_last(self) -> LinkedListNode[T] | None:
        """Deletes the last element of a linked list using only self.head."""

        def _remove_last(lst: LinkedListNode[T] | None) -> LinkedListNode[T] | None:
            if lst is None or lst.next is None:
                return None
            lst.next = _remove_last(lst.next)
            return lst

        return _remove_last(self.head)

    # def swap_nodes(self, node_data_1, node_data_2):
    #     if node_data_1 == node_data_2:
    #         return
    #     else:
    #         node_1 = self.head
    #         while node_1 is not None and node_1.data != node_data_1:
    #             node_1 = node_1.next

    #         node_2 = self.head
    #         while node_2 is not None and node_2.data != node_data_2:
    #             node_2 = node_2.next

    #         if node_1 is None or node_2 is None:
    #             return

    #         node_1.data, node_2.data = node_2.data, node_1.data
