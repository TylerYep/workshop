from typing import Set

from .hash_table import HashTable


class LinearProbingClean(HashTable):
    def __init__(self, num_buckets: int) -> None:
        self.table = [-1 for _ in range(num_buckets)]
        self.num_buckets = num_buckets
        self.capacity = num_buckets
        self.num_elems = 0

    def insert(self, data: int) -> bool:
        assert data >= 0
        if self.num_elems == self.capacity or self.contains(data):
            return False

        bucket = hash(data) % self.num_buckets
        while self.table[bucket] >= 0:
            if self.table[bucket] == data:
                return False
            bucket = (bucket + 1) % self.num_buckets

        self.table[bucket] = data
        self.num_elems += 1
        return True

    def _find_data(self, data: int) -> int:
        assert data >= 0
        bucket = hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index] == data:
                return index
            if self.table[index] == -1:
                break
        return -1

    def contains(self, data: int) -> bool:
        assert data >= 0
        return self._find_data(data) >= 0

    def remove(self, data: int) -> bool:
        assert data >= 0
        index = self._find_data(data)
        if index == -1:
            return False

        self.table[index] = -2
        self.num_elems -= 1
        return True

    def get_elems(self) -> Set[int]:
        return set(self.table)
