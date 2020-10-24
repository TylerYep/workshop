from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Tuple, TypeVar, Union
from uuid import UUID

T = TypeVar("T")


@dataclass(init=False)
class Heap(Generic[T]):
    def __bool__(self) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, item: T) -> bool:
        raise NotImplementedError

    def __ior__(self, other: object) -> None:
        raise NotImplementedError

    def enqueue(self, value: T, priority: float = 0) -> Union[T, UUID]:
        raise NotImplementedError

    def peek(self) -> Any:
        raise NotImplementedError

    def dequeue(self) -> Tuple[T, float]:
        raise NotImplementedError

    # def remove(self, value: Union[T, UUID]) -> None:
    #     raise NotImplementedError

    def merge(self, other: Heap[T]) -> None:
        raise NotImplementedError
