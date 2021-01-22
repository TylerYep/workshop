from .hash_table import HashTable


class LinearProbing(HashTable):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets)
        self.table = [-1 for _ in range(num_buckets)]

    def __contains__(self, data: int) -> bool:
        assert data >= 0
        return self._find_data(data) >= 0

    def insert(self, data: int) -> bool:
        assert data >= 0
        if self.num_elems == self.capacity or data in self:
            return False

        bucket = hash(data) % self.num_buckets
        while self.table[bucket] >= 0:
            if self.table[bucket] == data:
                return False
            bucket = (bucket + 1) % self.num_buckets

        self.table[bucket] = data
        self.num_elems += 1
        return True

    def remove(self, data: int) -> bool:
        assert data >= 0
        index = self._find_data(data)
        if index == -1:
            return False

        self.table[index] = -2
        self.num_elems -= 1
        return True

    def get_elems(self) -> set[int]:
        return set(self.table)

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
