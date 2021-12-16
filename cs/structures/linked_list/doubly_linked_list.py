from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(repr=False, slots=True)
class DoublyLinkedListNode(Generic[T]):
    data: T
    prev: DoublyLinkedListNode[T] | None = None
    next: DoublyLinkedListNode[T] | None = None

    def __repr__(self) -> str:
        return f"({self.data}) -> {self.next}"


@dataclass(init=False)
class DoublyLinkedList(Generic[T]):
    """
    - A linked list is similar to an array, it holds values. However, links
        in a linked list do not have indexes.
    - This is an example of a double ended, doubly linked list (or a deque).
    - Each link references the next link and the prev one.
    - A Doubly Linked List (DLL) contains an extra pointer, typically called
        prev pointer, together with next pointer and data which are
        there in singly linked list.
    - Advantages over SLL - It can be traversed in both forward and
        backward direction. Delete operation is more efficient.
    """

    head: DoublyLinkedListNode[T] | None

    def __init__(self) -> None:
        self.head: DoublyLinkedListNode[T] | None = None
        self.tail: DoublyLinkedListNode[T] | None = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[DoublyLinkedListNode[T]]:
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
    def from_list(cls, lst: list[T]) -> DoublyLinkedList[T]:
        linked_lst = cls()
        for item in reversed(lst):
            linked_lst.insert_at_head(item)
        return linked_lst

    def insert_at_head(self, data: T) -> None:
        new_node = DoublyLinkedListNode(data)
        self.size += 1
        if self.head is None or self.tail is None:
            self.tail = new_node
            self.head = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

    def insert_at_tail(self, data: T) -> None:
        new_node = DoublyLinkedListNode(data)
        self.size += 1
        if self.head is None or self.tail is None:
            self.tail = new_node
            self.head = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def pop_head(self) -> T:
        if self.head is None:
            raise Exception("List is empty")

        self.size -= 1
        head_data = self.head.data
        if self.head.next:
            self.head = self.head.next
            self.head.prev = None
        else:  # If there is no next prev node
            self.head = None
            self.tail = None
        return head_data

    def pop_tail(self) -> T:
        if self.head is None or self.tail is None:
            raise Exception("List is empty")

        self.size -= 1
        tail_data = self.tail.data
        if self.tail.prev is not None:
            self.tail = self.tail.prev
            self.tail.next = None
        else:  # if there is no prev node
            self.head = None
            self.tail = None
        return tail_data

    def remove(self, data: T) -> None:
        if self.head is None or self.tail is None:
            raise Exception("List is empty")

        current = self.head
        while current.data != data:  # Find the position to delete
            if current.next is not None:
                current = current.next
            else:  # We have reached the end an no value matches
                raise Exception("List does not contain value.")

        if current == self.head:
            _ = self.pop_head()
        elif current == self.tail:
            _ = self.pop_tail()
        else:
            self.size -= 1
            if current.prev is None or current.next is None:
                raise ValueError
            current.prev.next = current.next
            current.next.prev = current.prev
