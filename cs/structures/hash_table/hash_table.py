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


@dataslots
@dataclass
class HashTable(Generic[KT, VT]):
    """ This implementation assumes there are no duplicate keys. """

    num_buckets: int
    load_factor: float
    capacity: int = 0
    num_elems: int = 0

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
    def validate_key(key: KT) -> None:
        if key is None:
            raise ValueError("None cannot be inserted into a HashTable.")

    def insert(self, key: KT, value: VT) -> None:
        raise NotImplementedError

    def remove(self, key: KT) -> None:
        raise NotImplementedError

    def _find_key(self, key: KT) -> TableEntry[KT, VT] | None:
        raise NotImplementedError
