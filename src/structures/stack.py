from dataclasses import dataclass, field
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class Stack(Generic[T]):
    """ You should probably use the Python built-in List instead. """

    stack: List[T] = field(default_factory=list)

    def pop(self) -> T:
        if len(self.stack) == 0:
            raise IndexError
        return self.stack.pop()

    def push(self, item: T) -> None:
        self.stack.append(item)

    def peek(self) -> T:
        if len(self.stack) == 0:
            raise IndexError
        return self.stack[len(self.stack) - 1]

    def __len__(self) -> int:
        return len(self.stack)
