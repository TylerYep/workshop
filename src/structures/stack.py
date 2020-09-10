from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

from dataslots import with_slots

T = TypeVar("T")


@with_slots
@dataclass
class Stack(Generic[T]):
    """ You should probably use the Python built-in List instead. """

    _stack: List[T] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self._stack)

    def __len__(self) -> int:
        return len(self._stack)

    def __contains__(self, item: T) -> bool:
        return item in self._stack

    def push(self, item: T) -> None:
        self._stack.append(item)

    def pop(self) -> T:
        if not self._stack:
            raise IndexError
        return self._stack.pop()

    def peek(self) -> T:
        if not self._stack:
            raise IndexError
        return self._stack[-1]
