from typing import Generic, List, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    def __init__(self) -> None:
        self.queue: List[T] = []

    def add(self, item: T) -> None:
        self.queue.append(item)

    def remove(self) -> T:
        if len(self.queue) == 0:
            raise IndexError
        return self.queue.pop(0)

    def peek(self) -> T:
        if len(self.queue) == 0:
            raise IndexError
        return self.queue[0]

    def is_empty(self) -> bool:
        return not self.queue
