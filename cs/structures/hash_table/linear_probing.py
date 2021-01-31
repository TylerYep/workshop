from __future__ import annotations

from dataclasses import dataclass

from dataslots import dataslots

from .hash_table import KT, VT, HashTable, TableEntry


@dataslots
@dataclass
class LinearProbingEntry(TableEntry[KT, VT]):
    is_dead: bool = False


class LinearProbing(HashTable[KT, VT]):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets)
        self.table: list[LinearProbingEntry[KT, VT] | None] = [None] * num_buckets

    def __repr__(self) -> str:
        result = ""
        for i in range(self.num_buckets):
            entry = self.table[i]
            result += f"{i}  |  {None if entry is None else entry.value}\n"
        return result

    def insert(self, key: KT, value: VT) -> None:
        self.validate_key(key)
        if self.num_elems == self.capacity:
            raise KeyError

        bucket = hash(key) % self.num_buckets
        while (entry := self.table[bucket]) is not None and not entry.is_dead:
            if entry.key == key:
                raise KeyError
            bucket = (bucket + 1) % self.num_buckets

        self.table[bucket] = LinearProbingEntry(key, value)
        self.num_elems += 1

    def remove(self, key: KT) -> None:
        self.validate_key(key)
        if (entry := self._find_key(key)) is None:
            raise KeyError

        entry.is_dead = True
        self.num_elems -= 1

    def get_elems(self) -> list[tuple[KT, VT]]:
        return [(elem.key, elem.value) for elem in self.table if elem is not None]

    def _find_key(self, key: KT) -> LinearProbingEntry[KT, VT] | None:
        bucket = hash(key) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            entry = self.table[index]
            if entry is None:
                break
            if entry.key == key:
                return entry
        return None
