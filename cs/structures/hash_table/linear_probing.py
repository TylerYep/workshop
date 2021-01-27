from __future__ import annotations

from .hash_table import HashTable, T


class LinearProbing(HashTable[T]):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets)
        self.table: list[T | None] = [None] * num_buckets
        self.is_dead = [False] * num_buckets

    def __contains__(self, data: T) -> bool:
        self.validate_data(data)
        return self._find_data(data) is not None

    def __repr__(self) -> str:
        result = ""
        for i in range(self.num_buckets):
            result += f"{i}  |  {self.table[i]}\n"
        return result

    def insert(self, data: T) -> bool:
        self.validate_data(data)
        if self.num_elems == self.capacity or data in self:
            return False

        bucket = hash(data) % self.num_buckets
        while self.table[bucket] is not None and not self.is_dead[bucket]:
            if self.table[bucket] == data:
                return False
            bucket = (bucket + 1) % self.num_buckets

        self.table[bucket] = data
        self.num_elems += 1
        return True

    def remove(self, data: T) -> bool:
        self.validate_data(data)
        index = self._find_data(data)
        if index is None:
            return False

        self.is_dead[index] = True
        self.num_elems -= 1
        return True

    def get_elems(self) -> set[T]:
        return {elem for elem in self.table if elem is not None}

    def _find_data(self, data: T) -> int | None:
        bucket = hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index] == data:
                return index
            if self.table[index] is None:
                break
        return None
