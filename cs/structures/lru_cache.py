from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, ClassVar, Generic, NamedTuple, ParamSpec, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")
P = ParamSpec("P")
R = TypeVar("R")


class CacheInfo(NamedTuple):
    hits: int
    misses: int
    capacity: int
    current_size: int


class LRUCache(Generic[KT, VT]):
    """Uses a regular dictionary and the fact that dictionaries are ordered."""

    # Class variable maps the decorator functions to their respective instance
    # ClassVar[dict[Callable[..., Any], LRUCache[KT, VT]]]
    decorator_instance_map: ClassVar[dict[Callable[..., Any], LRUCache[Any, Any]]] = {}

    def __init__(self, max_capacity: int) -> None:
        self.cache: dict[KT, VT] = {}
        self.max_capacity = max_capacity
        self.hits = 0
        self.misses = 0

    def __getitem__(self, key: KT) -> VT | None:
        if key in self.cache:
            self.hits += 1
            # Equivalent to OrderedDict:  self.cache.move_to_end(key)
            self.cache[key] = self.cache.pop(key)
            return self.cache[key]

        self.misses += 1
        return None

    def __setitem__(self, key: KT, val: VT) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = val
        if len(self.cache) > self.max_capacity:
            # Equivalent to OrderedDict:  self.cache.popitem(last=False)
            self.cache.pop(next(iter(self.cache)))

    def __bool__(self) -> bool:
        return bool(self.cache)

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, key: KT) -> bool:
        return key in self.cache

    def __repr__(self) -> str:
        return str(
            CacheInfo(self.hits, self.misses, self.max_capacity, len(self.cache))
        )

    @classmethod
    def lru_cache(cls, size: int = 128) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def cache_decorator_inner(func: Callable[P, R]) -> Callable[P, R]:
            @wraps(func)
            def cache_decorator_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                if func not in cls.decorator_instance_map:
                    cls.decorator_instance_map[func] = LRUCache(size)

                result = cls.decorator_instance_map[func][args]
                if result is None:
                    result = func(*args, **kwargs)
                    cls.decorator_instance_map[func][args] = result
                return result

            def cache_info() -> LRUCache[KT, VT]:
                return cls.decorator_instance_map[func]

            cache_decorator_wrapper.cache_info = cache_info  # type: ignore[attr-defined]  # noqa: E501
            return cache_decorator_wrapper

        return cache_decorator_inner


def lru_cache(size: int = 128) -> Callable[[Callable[P, R]], Callable[P, R]]:
    return LRUCache.lru_cache(size)
