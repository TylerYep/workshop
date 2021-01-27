from __future__ import annotations

import math
import random
from collections.abc import Callable
from typing import cast

from .hash_table import HashTable, T

_memomask: dict[int, int] = {}


def hash_function(n: int) -> Callable[[T], int]:
    mask = _memomask.get(n)
    if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)

    def myhash(x: T) -> int:
        return hash(x) ^ cast(int, mask)

    return myhash


class Cuckoo(HashTable[T]):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets // 2)
        self.table_1: list[T | None] = [None] * self.num_buckets
        self.table_2 = list(self.table_1)
        self.curr_hash_fn_num = 1
        self.hash_1 = hash_function(self.curr_hash_fn_num)
        self.hash_2 = hash_function(self.curr_hash_fn_num + 1)
        self.rehashing_depth_limit = int(6 * math.log(num_buckets * 2))

    def __contains__(self, data: T) -> bool:
        self.validate_data(data)
        bucket = self.hash_1(data) % self.num_buckets
        if self.table_1[bucket] == data:
            return True

        bucket = self.hash_2(data) % self.num_buckets
        if self.table_2[bucket] == data:
            return True

        return False

    def __repr__(self) -> str:
        max_width = 20
        result = ""
        for i in range(self.num_buckets):
            table_row_1 = f"{i}  |  {self.table_1[i]}"
            table_row_2 = f"{i}  |  {self.table_2[i]}"
            result += f"{table_row_1:<{max_width}} {table_row_2}\n"
        return result

    def insert(self, data: T) -> bool:
        self.validate_data(data)
        if data in self:
            return False

        use_table_1 = True
        curr: T | None = data
        # Try inserting data, swapping items up to the given depth limit.
        for _ in range(self.rehashing_depth_limit):
            if use_table_1:
                bucket = self.hash_1(curr) % self.num_buckets
                if self.table_1[bucket] is None:
                    self.table_1[bucket] = curr
                    return True
                curr, self.table_1[bucket] = self.table_1[bucket], curr

            else:
                bucket = self.hash_2(curr) % self.num_buckets
                if self.table_2[bucket] is None:
                    self.table_2[bucket] = curr
                    return True
                curr, self.table_2[bucket] = self.table_2[bucket], curr

            use_table_1 = not use_table_1

        # Rehash using a new hash function and recurse to try insert again.
        self.curr_hash_fn_num += 1
        self.hash_1 = hash_function(self.curr_hash_fn_num)
        self.hash_2 = hash_function(self.curr_hash_fn_num + 1)

        # Copy all old elements to a temp table
        table = [item for item in self.table_1 + self.table_2 if item is not None]

        # Clear both tables
        self.table_1 = [None] * self.num_buckets
        self.table_2 = list(self.table_1)

        for item in table:
            self.insert(item)

        return True

    def remove(self, data: T) -> bool:
        self.validate_data(data)
        bucket = self.hash_1(data) % self.num_buckets
        if self.table_1[bucket] == data:
            self.table_1[bucket] = None
            return True

        bucket = self.hash_2(data) % self.num_buckets
        if self.table_2[bucket] == data:
            self.table_2[bucket] = None
            return True

        return False
