import math

import pytest
from bitarray import bitarray

from cs.structures import BloomFilter


class TestBloomFilter:
    @staticmethod
    def test_stats() -> None:
        N = 20
        bloom = BloomFilter[int](n=20, p=0.2)
        for i in range(N):
            bloom.add(i)

        assert bloom.k == 3
        assert bloom.m == 67
        assert bloom.array == bitarray(
            "1010110110101011011101101110111101110111101011011000111111101110000"
        )

    @staticmethod
    def test_str() -> None:
        N = 5
        bloom = BloomFilter[int](n=5, p=0.2)
        for i in range(N):
            bloom.add(i)
        assert str(bloom) == "BloomFilter(01001101101010111)"

    @staticmethod
    @pytest.mark.parametrize(
        ("n", "p"), [(100, 0.05), (500, 0.01), (1000, 0.005), (5000, 0.002)]
    )
    def test_bloom_filter(n: int, p: float) -> None:
        N = 100
        bloom = BloomFilter[int](n, p)
        assert repr(bloom) == f"BloomFilter(n={n}, p={p})"
        assert bool(bloom) is False

        for i in range(N):
            bloom.add(i)
            assert i in bloom

        assert bool(bloom) is True
        assert len(bloom) == N
        assert math.isclose(bloom.approx_items(), N, rel_tol=0.05)
        assert math.isclose(bloom.calculate_p(), p, abs_tol=p)

        false_pos = sum(i in bloom for i in range(n, n + N))
        assert math.isclose(false_pos / N, p, abs_tol=p)
