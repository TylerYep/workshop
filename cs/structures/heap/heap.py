from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Self

from cs.util import Comparable

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(init=False)
class Heap[T: Comparable]:
    def __bool__(self) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, item: T) -> bool:
        raise NotImplementedError

    def __ior__(self, other: object) -> Self:
        raise NotImplementedError

    def __getitem__(self, value: T | UUID) -> Any:
        raise NotImplementedError

    def enqueue(self, value: T, priority: float = 0) -> T | UUID:
        raise NotImplementedError

    def peek(self) -> tuple[T, float]:
        raise NotImplementedError

    def dequeue(self) -> tuple[T, float]:
        raise NotImplementedError

    def merge(self, other: Heap[T]) -> None:
        raise NotImplementedError
