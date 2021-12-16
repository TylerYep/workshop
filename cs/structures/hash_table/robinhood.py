from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .hash_table import KT, VT, HashTable, TableEntry


@dataclass(slots=True)
class RobinHoodEntry(TableEntry[KT, VT]):
    dist: int = -1

    def __repr__(self) -> str:
        return f"({self.value}, {self.dist})"


class RobinHood(HashTable[KT, VT]):
    def __init__(self, num_buckets: int, load_factor: float = 0.4) -> None:
        super().__init__(num_buckets, load_factor)
        self.table: list[RobinHoodEntry[KT, VT] | None] = [None] * num_buckets
        self.hash: Callable[[KT], int] = lambda x: hash(x) % num_buckets

    def __str__(self) -> str:
        result = ""
        for i in range(self.num_buckets):
            entry = self.table[i]
            result += f"{i}  |  {None if entry is None else entry.value}\n"
        return result

    def insert(self, key: KT, value: VT) -> None:
        self.validate_key(key)
        # Replace existing key
        if (entry := self._find_key(key)) is not None:
            entry.value = value
            return

        # Resize table if size exceeds capacity.
        if self.num_elems >= self.load_factor * self.capacity:
            self.capacity *= 2
            self.num_buckets *= 2
            self.num_elems = 0
            table = list(self.table)
            self.table = [None] * self.num_buckets
            for entry in table:
                if entry is not None:
                    self.insert(entry.key, entry.value)

        bucket = self.hash(key) % self.num_buckets
        curr: RobinHoodEntry[KT, VT] | None = RobinHoodEntry(key, value)
        curr_dist = 0
        while curr is not None and (
            (entry := self.table[bucket]) is None or curr.key != entry.key
        ):
            if entry is None or entry.dist < curr_dist:
                self.table[bucket] = RobinHoodEntry(curr.key, curr.value, curr_dist)
                curr, curr_dist = entry, -1 if entry is None else entry.dist
            curr_dist += 1
            bucket = (bucket + 1) % self.num_buckets
        self.num_elems += 1

    def remove(self, key: KT) -> None:
        self.validate_key(key)
        bucket = self.hash(key) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            entry = self.table[index]
            if entry is None:
                break
            if entry.key == key:
                self._backward_shift(index)
                self.num_elems -= 1
                return
        raise KeyError

    def _backward_shift(self, i: int) -> None:
        j = (i + 1) % self.num_buckets
        entry = self.table[j]
        while entry is not None and entry.dist > 0:
            entry.dist -= 1
            self.table[i], entry = entry, self.table[i]
            i, j = j, (i + 1) % self.num_buckets
        self.table[i] = None

    def _find_key(self, key: KT) -> RobinHoodEntry[KT, VT] | None:
        bucket = self.hash(key) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            entry = self.table[index]
            if entry is not None and entry.key == key:
                return entry
            if entry is None or entry.dist < i:
                break
        return None
