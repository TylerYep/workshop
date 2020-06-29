import math
import random
from typing import Dict, Callable
from .hash_table import HashTable


_memomask: Dict[int, int] = {}

def hash_function(n: int) -> Callable[[int], int]:
    mask = _memomask.get(n)
    if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)
    def myhash(x: int) -> int:
        return hash(x) ^ mask
    return myhash


class Cuckoo(HashTable):
    def __init__(self, num_buckets: int) -> None:
        self.num_buckets = num_buckets // 2
        self.table_1 = [-1 for _ in range(self.num_buckets)]
        self.table_2 = list(self.table_1)
        self.curr_hash_fn_num = 1
        self.hash_1 = hash_function(self.curr_hash_fn_num)
        self.hash_2 = hash_function(self.curr_hash_fn_num + 1)

    def insert(self, data: int) -> bool:
        assert data >= 0

        if self.contains(data):
            return False

        use_table_1 = True
        depth = 0

        while depth < 6 * math.log(self.num_buckets * 2):
            if use_table_1:
                bucket = self.hash_1(data) % self.num_buckets
                if self.table_1[bucket] == -1:
                    self.table_1[bucket] = data
                    return True
                data, self.table_1[bucket] = self.table_1[bucket], data

            else:
                bucket = self.hash_2(data) % self.num_buckets
                if self.table_2[bucket] == -1:
                    self.table_2[bucket] = data
                    return True
                data, self.table_2[bucket] = self.table_2[bucket], data

            use_table_1 = not use_table_1
            depth += 1

        # Rehash
        self.curr_hash_fn_num += 1
        self.hash_1 = hash_function(self.curr_hash_fn_num)
        self.hash_2 = hash_function(self.curr_hash_fn_num + 1)

        # Copy all old elements to two temp tables
        table_1 = list(self.table_1)
        table_2 = list(self.table_2)

        # Clear both tables
        self.table_1 = [-1 for _ in range(self.num_buckets)]
        self.table_2 = list(self.table_1)

        for item in table_1 + table_2:
            if item >= 0:
                self.insert(item)

        return True


    def contains(self, data: int) -> bool:
        assert data >= 0
        bucket = self.hash_1(data) % self.num_buckets
        if self.table_1[bucket] == data:
            return True

        bucket = self.hash_2(data) % self.num_buckets
        if self.table_2[bucket] == data:
            return True

        return False

    def remove(self, data: int) -> bool:
        assert data >= 0

        bucket = self.hash_1(data) % self.num_buckets
        if self.table_1[bucket] == data:
            self.table_1[bucket] = -1
            return True

        bucket = self.hash_2(data) % self.num_buckets
        if self.table_2[bucket] == data:
            self.table_2[bucket] = -1
            return True

        return False

    def __repr__(self) -> str:
        widths = [max(
            len(str(self.table_1[i])) + int(self.table_1[i] < 0) - 1,
            len(str(self.table_2[i])) + int(self.table_2[i] < 0) - 1
        ) for i in range(self.num_buckets)]
        indices = "  |  ".join([f"{i:{widths[i]}}" for i in range(self.num_buckets)])
        table1 = "  |  ".join([f"{self.table_1[i]:{widths[i]}}" for i in range(self.num_buckets)])
        table2 = "  |  ".join([f"{self.table_2[i]:{widths[i]}}" for i in range(self.num_buckets)])
        return f"\n{indices}\n{'---' * sum(widths)}\n{table1}\n{table2}\n"
