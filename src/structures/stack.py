from typing import Generic, List, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self.stack: List[T] = []

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
