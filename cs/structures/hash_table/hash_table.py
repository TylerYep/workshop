from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from dataslots import dataslots

KT = TypeVar("KT")
VT = TypeVar("VT")


@dataslots
@dataclass
class TableEntry(Generic[KT, VT]):
    key: KT
    value: VT

    def __repr__(self) -> str:
        return str(self.key)


class HashTable(Generic[KT, VT]):
    """ This implementation assumes there are no duplicate keys. """

    def __init__(self, num_buckets: int) -> None:
        self.num_buckets = num_buckets
        self.capacity = num_buckets
        self.num_elems = 0

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
    def validate_key(key: KT) -> None:
        if key is None:
            raise ValueError("None cannot be inserted into a HashTable.")

    def insert(self, key: KT, value: VT) -> None:
        raise NotImplementedError

    def remove(self, key: KT) -> None:
        raise NotImplementedError

    def _find_key(self, key: KT) -> TableEntry[KT, VT] | None:
        raise NotImplementedError
