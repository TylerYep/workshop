from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class Queue(Generic[T]):
    """ You should probably use the Python built-in List instead. """

    queue: List[T] = field(default_factory=list)

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
