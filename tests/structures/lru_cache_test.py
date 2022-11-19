from cs.structures import LRUCache, lru_cache


class TestLRUCache:
    @staticmethod
    def test_lru_cache() -> None:
        cache = LRUCache[int, int](2)
        assert (1 in cache) is False
        cache[1] = 1
        cache[2] = 2

        assert (1 in cache) is True
        assert cache[1] == 1

        cache[3] = 3

        assert cache[2] is None

        cache[4] = 4

        assert cache[1] is None
        assert cache[3] == 3  # type: ignore[unreachable]
        assert cache[4] == 4

        assert str(cache) == "CacheInfo(hits=3, misses=2, capacity=2, current_size=2)"

        @lru_cache(100)
        def fib(num: int) -> int:
            if num in (1, 2):
                return 1
            return fib(num - 1) + fib(num - 2)

        for i in range(1, 100):
            _ = fib(i)

        assert (
            str(fib.cache_info())
            == "CacheInfo(hits=194, misses=99, capacity=100, current_size=99)"
        )
