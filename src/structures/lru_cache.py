from __future__ import annotations

from collections import OrderedDict
from typing import Any, Mapping, Optional, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class LRUCache(Mapping[KT, VT]):
    def __init__(self, max_capacity: int) -> None:
        self.max_capacity = max_capacity
        self.cache: OrderedDict[KT, VT] = OrderedDict()  # pylint: disable=unsubscriptable-object

    def __getitem__(self, key: KT) -> VT:
        if key not in self.cache:
            raise ValueError
        val = self.cache[key]
        self.cache.move_to_end(key)
        return val

    def __setitem__(self, key: KT, val: VT) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = val
        if len(self.cache) > self.max_capacity:
            self.cache.popitem(last=False)
