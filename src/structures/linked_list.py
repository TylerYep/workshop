from __future__ import annotations

from typing import Optional


class LinkedListNode:
    def __init__(self, data: int, next_node: Optional[LinkedListNode]) -> None:
        self.data = data
        self.next = next_node

    def __repr__(self) -> str:
        return f"({self.data}) -> {self.next}"


def remove_last(l: LinkedListNode) -> Optional[LinkedListNode]:
    """ Deletes the last element of a linked list. """
    if l is None or l.next is None:
        return None
    l.next = remove_last(l.next)
    return l


if __name__ == "__main__":
    head = LinkedListNode(0, None)
    curr = head
    for i in range(1, 10):
        curr.next = LinkedListNode(i, None)
        curr = curr.next
    print(head)
    remove_last(head)
    print(head)
    remove_last(head)
    print(head)
