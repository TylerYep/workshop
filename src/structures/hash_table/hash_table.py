from typing import Any, List


class HashTable:
    def __init__(self, num_buckets: int) -> None:
        self.table: List[Any] = []
        self.num_buckets = num_buckets
        self.capacity = num_buckets
        self.num_elems = 0

    def __contains__(self, data: int) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        widths = [
            len(str(self.table[i])) + int(self.table[i] < 0) - 1
            for i in range(self.num_buckets)
        ]
        indices = "  |  ".join([f"{i:{widths[i]}}" for i in range(self.num_buckets)])
        table = "  |  ".join([str(self.table[i]) for i in range(self.num_buckets)])
        return f"\n{indices}\n{'---' * sum(widths)}\n{table}\n"

    def insert(self, data: int) -> bool:
        raise NotImplementedError

    def remove(self, data: int) -> bool:
        raise NotImplementedError
