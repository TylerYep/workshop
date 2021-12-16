from __future__ import annotations

from dataclasses import dataclass

from .hash_table import KT, VT, HashTable, TableEntry


@dataclass(slots=True)
class LinearProbingEntry(TableEntry[KT, VT]):
    is_dead: bool = False


class LinearProbing(HashTable[KT, VT]):
    def __init__(self, num_buckets: int, load_factor: float = 0.4) -> None:
        super().__init__(num_buckets, load_factor)
        self.table: list[LinearProbingEntry[KT, VT] | None] = [None] * num_buckets

    def __str__(self) -> str:
        result = ""
        for i in range(self.num_buckets):
            entry = self.table[i]
            output = None if entry is None or entry.is_dead else entry.value
            result += f"{i}  |  {output}\n"
        return result

    def insert(self, key: KT, value: VT) -> None:
        self.validate_key(key)
        # Skip check for duplicates because membership check is very slow.

        # Resize table if size exceeds capacity.
        if self.num_elems >= self.load_factor * self.capacity:
            self.capacity *= 2
            self.num_buckets *= 2
            self.num_elems = 0
            table = list(self.table)
            self.table = [None] * self.num_buckets
            for entry in table:
                if entry is not None and not entry.is_dead:
                    self.insert(entry.key, entry.value)

        bucket = hash(key) % self.num_buckets
        while (entry := self.table[bucket]) is not None and not entry.is_dead:
            # Replace existing key
            if entry.key == key:
                entry.value = value
                return
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
            if entry.key == key and not entry.is_dead:
                return entry
        return None
