from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic

from dataslots import dataslots

from .hash_table import HashTable, T


@dataslots
@dataclass
class Pair(Generic[T]):
    val: T | None = None
    dist: int = -1

    def __repr__(self) -> str:
        return f"({self.val}, {self.dist})"


class RobinHood(HashTable[T]):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets)
        self.table: list[Pair[T]] = [Pair() for _ in range(num_buckets)]
        self.hash: Callable[[T], int] = lambda x: hash(x) % num_buckets

    def __contains__(self, data: T) -> bool:
        self.validate_data(data)
        bucket = self.hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index].val == data:
                return True

            if self.table[index].val is None or self.table[index].dist < i:
                break
        return False

    def __repr__(self) -> str:
        result = ""
        for i in range(self.num_buckets):
            result += f"{i}  |  {self.table[i].val}\n"
        return result

    def insert(self, data: T) -> bool:
        self.validate_data(data)
        if self.num_elems == self.capacity:
            return False

        bucket = self.hash(data) % self.num_buckets
        curr: T | None = data
        curr_dist = 0
        while curr not in (self.table[bucket].val, -1):
            if self.table[bucket].val is None or self.table[bucket].dist < curr_dist:
                temp = self.table[bucket]
                self.table[bucket] = Pair(curr, curr_dist)
                curr, curr_dist = temp.val, temp.dist
            curr_dist += 1
            bucket = (bucket + 1) % self.num_buckets

        self.num_elems += 1
        return True

    def remove(self, data: T) -> bool:
        self.validate_data(data)
        bucket = self.hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index].val == data:
                self._backward_shift(index)
                self.num_elems -= 1
                return True
            if self.table[index].val is None:
                break
        return False

    def _backward_shift(self, index: int) -> None:
        next_index = (index + 1) % self.num_buckets
        while (
            self.table[next_index].val is not None and self.table[next_index].dist > 0
        ):
            self.table[index], self.table[next_index] = (
                self.table[next_index],
                self.table[index],
            )
            self.table[index].dist -= 1
            index = next_index
            next_index = (index + 1) % self.num_buckets
        self.table[index] = Pair()
