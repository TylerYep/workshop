from collections.abc import Callable
from dataclasses import dataclass

from dataslots import dataslots

from .hash_table import HashTable


@dataslots
@dataclass
class Pair:
    val: int = -1
    dist: int = -1

    def __repr__(self) -> str:
        return f"({self.val}, {self.dist})"


class RobinHood(HashTable):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets)
        self.table: list[Pair] = [Pair() for _ in range(num_buckets)]
        self.hash: Callable[[int], int] = lambda x: x % num_buckets

    def __contains__(self, data: int) -> bool:
        assert data >= 0
        bucket = self.hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index].val == data:
                return True

            if self.table[index].val == -1 or self.table[index].dist < i:
                break
        return False

    def __repr__(self) -> str:
        widths = [len(str(self.table[i])) for i in range(self.num_buckets)]
        indices = "  |  ".join([f"{i:{widths[i]}}" for i in range(self.num_buckets)])
        table = "  |  ".join([str(self.table[i]) for i in range(self.num_buckets)])
        return f"\n{indices}\n{'--' * sum(widths)}\n{table}\n"

    def insert(self, data: int) -> bool:
        assert data >= 0
        if self.num_elems == self.capacity:
            return False

        curr_dist = 0
        bucket = self.hash(data) % self.num_buckets
        while data not in (self.table[bucket].val, -1):
            if self.table[bucket].val == -1 or self.table[bucket].dist < curr_dist:
                temp = self.table[bucket]
                self.table[bucket] = Pair(data, curr_dist)
                data, curr_dist = temp.val, temp.dist
            curr_dist += 1
            bucket = (bucket + 1) % self.num_buckets

        self.num_elems += 1
        return True

    def backward_shift(self, index: int) -> None:
        next_index = (index + 1) % self.num_buckets
        while self.table[next_index].val != -1 and self.table[next_index].dist > 0:
            self.table[index], self.table[next_index] = (
                self.table[next_index],
                self.table[index],
            )
            self.table[index].dist -= 1
            index = next_index
            next_index = (index + 1) % self.num_buckets
        self.table[index] = Pair()

    def remove(self, data: int) -> bool:
        assert data >= 0
        bucket = self.hash(data) % self.num_buckets
        for i in range(self.num_buckets):
            index = (bucket + i) % self.num_buckets
            if self.table[index].val == data:
                self.backward_shift(index)
                self.num_elems -= 1
                return True
            if self.table[index].val == -1:
                break
        return False

    def get_elems(self) -> set[int]:
        return {x.val for x in self.table}
