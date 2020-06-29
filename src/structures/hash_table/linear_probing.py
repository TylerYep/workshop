from typing import Set

from .hash_table import HashTable


class LinearProbing(HashTable):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets)
        self.table = [-1 for _ in range(num_buckets)]

    def insert(self, data: int) -> None:
        assert data >= 0
        bucket = hash(data) % self.num_buckets
        while self.table[bucket] >= 0:
            if self.table[bucket] == data:
                return
            bucket = (bucket + 1) % self.num_buckets
        self.table[bucket] = data

    def contains(self, data: int) -> bool:
        assert data >= 0
        bucket = hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index] == data:
                return True
            if self.table[index] == -1:
                break
        return False

    def remove(self, data: int) -> None:
        assert data >= 0
        bucket = hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index] == data:
                self.table[index] = -2
                return
            if self.table[index] == -1:
                break

    def get_elems(self) -> Set[int]:
        return set(self.table)
