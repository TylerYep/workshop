from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar, cast

KT = TypeVar("KT")
VT = TypeVar("VT")


@dataclass(slots=True)
class TableEntry(Generic[KT, VT]):
    key: KT
    value: VT

    def __repr__(self) -> str:
        return str(self.key)


@dataclass(slots=True)
class HashTable(Generic[KT, VT]):
    """This implementation assumes there are no duplicate keys."""

    num_buckets: int
    load_factor: float
    capacity: int = 0
    num_elems: int = 0
    _hash_ids: ClassVar[dict[int, int]] = {}

    def __post_init__(self) -> None:
        self.capacity = self.num_buckets

    def __bool__(self) -> bool:
        return self.num_elems > 0

    def __len__(self) -> int:
        return self.num_elems

    def __contains__(self, key: KT) -> bool:
        self.validate_key(key)
        return self._find_key(key) is not None

    def __getitem__(self, key: KT) -> VT:
        if (result := self._find_key(key)) is None:
            raise KeyError
        return result.value

    def __setitem__(self, key: KT, value: VT) -> None:
        self.insert(key, value)

    def __delitem__(self, key: KT) -> None:
        self.remove(key)

    @staticmethod
    def generate_hash_function(n: int | None = None) -> Callable[[KT], int]:
        if n is None:
            n = max(HashTable._hash_ids) + 1 if HashTable._hash_ids else 0
        mask = HashTable._hash_ids.get(n)
        if mask is None:
            mask = HashTable._hash_ids[n] = random.getrandbits(32)
        return lambda x: hash(x) ^ cast(int, mask)

    @staticmethod
    def validate_key(key: KT) -> None:
        if key is None:
            raise ValueError("None cannot be inserted into a HashTable.")

    def insert(self, key: KT, value: VT) -> None:
        raise NotImplementedError

    def remove(self, key: KT) -> None:
        raise NotImplementedError

    def _find_key(self, key: KT) -> TableEntry[KT, VT] | None:
        raise NotImplementedError
