from __future__ import annotations

import math
import random
from collections.abc import Callable
from typing import cast

from .hash_table import KT, VT, HashTable, TableEntry

_memomask: dict[int, int] = {}


def hash_function(n: int) -> Callable[[KT], int]:
    mask = _memomask.get(n)
    if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)

    def myhash(x: KT) -> int:
        return hash(x) ^ cast(int, mask)

    return myhash


class Cuckoo(HashTable[KT, VT]):
    def __init__(self, num_buckets: int) -> None:
        super().__init__(num_buckets)
        self.num_buckets //= 2
        if self.num_buckets <= 1:
            self.num_buckets += 1

        self.table_1: list[TableEntry[KT, VT] | None] = [None] * self.num_buckets
        self.table_2 = list(self.table_1)
        self.curr_hash_fn_num = 1
        self.hash_1 = hash_function(self.curr_hash_fn_num)
        self.hash_2 = hash_function(self.curr_hash_fn_num + 1)
        self.rehashing_depth_limit = int(6 * math.log(num_buckets * 2))

    def __repr__(self) -> str:
        max_width = 20
        result = ""
        for i in range(self.num_buckets):
            table_row_1 = f"{i}  |  {self.table_1[i]}"
            table_row_2 = f"{i}  |  {self.table_2[i]}"
            result += f"{table_row_1:<{max_width}} {table_row_2}\n"
        return result

    def insert(self, key: KT, value: VT) -> None:
        if self.num_elems == self.capacity or self._find_key(key) is not None:
            raise KeyError
        self._insert(key, value)
        self.num_elems += 1

    def remove(self, key: KT) -> None:
        self.validate_key(key)
        self.num_elems -= 1
        bucket = self.hash_1(key) % self.num_buckets
        entry = self.table_1[bucket]
        if entry is not None and entry.key == key:
            self.table_1[bucket] = None
            return

        bucket = self.hash_2(key) % self.num_buckets
        entry = self.table_2[bucket]
        if entry is not None and entry.key == key:
            self.table_2[bucket] = None

    def _insert(self, key: KT, value: VT) -> None:
        self.validate_key(key)

        use_table_1 = True
        curr: TableEntry[KT, VT] | None = TableEntry(key, value)
        # Try inserting key, swapping items up to the given depth limit.
        for _ in range(self.rehashing_depth_limit):
            if curr is None:
                raise RuntimeError

            if use_table_1:
                bucket = self.hash_1(curr.key) % self.num_buckets
                if self.table_1[bucket] is None:
                    self.table_1[bucket] = curr
                    return
                curr, self.table_1[bucket] = self.table_1[bucket], curr

            else:
                bucket = self.hash_2(curr.key) % self.num_buckets
                if self.table_2[bucket] is None:
                    self.table_2[bucket] = curr
                    return
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
            self._insert(item.key, item.value)

    def _find_key(self, key: KT) -> TableEntry[KT, VT] | None:
        bucket = self.hash_1(key) % self.num_buckets
        entry = self.table_1[bucket]
        if entry is not None and entry.key == key:
            return entry

        bucket = self.hash_2(key) % self.num_buckets
        entry = self.table_2[bucket]
        if entry is not None and entry.key == key:
            return entry

        return None
