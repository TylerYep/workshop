from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Queue(Generic[T]):
    """You should probably use the Python built-in list or deque instead."""

    _queue: list[T] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self._queue)

    def __len__(self) -> int:
        return len(self._queue)

    def __contains__(self, item: T) -> bool:
        return item in self._queue

    def enqueue(self, item: T) -> None:
        self._queue.append(item)

    def dequeue(self) -> T:
        if not self._queue:
            raise IndexError
        return self._queue.pop(0)

    def peek(self) -> T:
        if not self._queue:
            raise IndexError
        return self._queue[0]
