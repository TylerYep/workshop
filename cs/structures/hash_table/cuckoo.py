from __future__ import annotations

import math

from .hash_table import KT, VT, HashTable, TableEntry


class Cuckoo(HashTable[KT, VT]):
    """
    A hash system with worst-case constant-time lookup and deletion, and amortized
    expected O(1) insertion.

    Cuckoo hashing works by maintaining two arrays and two universal hash functions f
    and g. When an element x is inserted, the value f(x) is computed and the entry is
    stored in that index in the first array. If that spot was initially empty, we are
    done. Otherwise, the element y that was already there is "kicked out." We then
    compute g(y) and store element y at position g(y) in the second array, which may in
    turn kick out another element, which will be stored in the first array. This process
    repeats until either a loop is detected (in which case we pick a new hash function
    and rehash), or all elements finally come to rest.
    """

    def __init__(self, num_buckets: int, load_factor: float = 0.4) -> None:
        super().__init__(num_buckets, load_factor)
        self.num_buckets //= 2
        if self.num_buckets <= 1:
            self.num_buckets += 1

        self.table_1: list[TableEntry[KT, VT] | None] = [None] * self.num_buckets
        self.table_2 = list(self.table_1)
        self.hash_1 = self.generate_hash_function()
        self.hash_2 = self.generate_hash_function()
        self.rehashing_depth_limit = int(6 * math.log(num_buckets * 2))

    def __str__(self) -> str:
        max_width = 20
        result = ""
        for i in range(self.num_buckets):
            table_row_1 = f"{i}  |  {self.table_1[i]}"
            table_row_2 = f"{i}  |  {self.table_2[i]}"
            result += f"{table_row_1:<{max_width}} {table_row_2}\n"
        return result

    def insert(self, key: KT, value: VT) -> None:
        self.validate_key(key)
        # Replace existing key
        if (entry := self._find_key(key)) is not None:
            entry.value = value
            return

        # Resize table if size exceeds capacity.
        if self.num_elems >= self.load_factor * self.capacity:
            self.capacity *= 2
            self.num_buckets *= 2
            self._rehash()

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

        self._rehash()

    def _rehash(self) -> None:
        # Rehash using a new hash function and recurse to try insert again.
        self.hash_1 = self.generate_hash_function()
        self.hash_2 = self.generate_hash_function()

        # Copy all old elements to a temp table
        table = [item for item in self.table_1 + self.table_2 if item is not None]

        # Clear both tables
        self.table_1 = [None] * self.num_buckets
        self.table_2 = list(self.table_1)

        # Reinsert all elements
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
