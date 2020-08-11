from __future__ import annotations

from collections import OrderedDict

# from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Optional, TypeVar, no_type_check

KT = TypeVar("KT")
VT = TypeVar("VT")


# @dataclass
class LRUCache(Generic[KT, VT]):
    """ Must use an OrderedDict in order to use the move_to_end() command """

    # class variable to map the decorator functions to their respective instance
    decorator_instance_map: Dict[Callable[..., Any], LRUCache[KT, VT]] = {}

    def __init__(self, max_capacity: int) -> None:
        self.cache: OrderedDict[KT, VT] = OrderedDict()  # pylint: disable=unsubscriptable-object
        self.max_capacity = max_capacity
        self.hits = 0
        self.miss = 0

    def __getitem__(self, key: KT) -> Optional[VT]:
        if key in self.cache:
            self.hits += 1
            self.cache.move_to_end(key)
            return self.cache[key]

        self.miss += 1
        return None

    def __setitem__(self, key: KT, val: VT) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = val
        if len(self.cache) > self.max_capacity:
            self.cache.popitem(last=False)

    def __contains__(self, key: KT) -> bool:
        return key in self.cache

    def __repr__(self) -> str:
        return (
            f"CacheInfo(hits={self.hits}, misses={self.miss}, "
            f"capacity={self.max_capacity}, current_size={len(self.cache)})"
        )


@no_type_check
def lru_cache(size: int = 128) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def cache_decorator_inner(func: Callable[..., Any]) -> Callable[..., Any]:
        def cache_decorator_wrapper(*args: Any, **kwargs: Any) -> Any:
            if func not in LRUCache.decorator_instance_map:
                LRUCache.decorator_instance_map[func] = LRUCache(size)

            result = LRUCache.decorator_instance_map[func][args]
            if result is None:
                result = func(*args, **kwargs)
                LRUCache.decorator_instance_map[func][args] = result
            return result

        def cache_info() -> LRUCache[KT, VT]:
            return LRUCache.decorator_instance_map[func]

        cache_decorator_wrapper.cache_info = cache_info
        return cache_decorator_wrapper

    return cache_decorator_inner
