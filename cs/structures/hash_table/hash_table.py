from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class HashTable(Generic[T]):
    def __init__(self, num_buckets: int) -> None:
        self.num_buckets = num_buckets
        self.capacity = num_buckets
        self.num_elems = 0

    def __contains__(self, data: T) -> bool:
        raise NotImplementedError

    @staticmethod
    def validate_data(data: T) -> None:
        if data is None:
            raise ValueError("None cannot be inserted into a HashTable.")

    def insert(self, data: T) -> bool:
        raise NotImplementedError

    def remove(self, data: T) -> bool:
        raise NotImplementedError
