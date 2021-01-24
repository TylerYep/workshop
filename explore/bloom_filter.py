import math

from cs.structures import BloomFilter


def bloom_filter_stats(n: int, p: float) -> None:
    print("Bloom Filter:")
    print(f"capacity     n = {n}")
    print(f"given        p = {p}")
    b = BloomFilter[int](n, p)
    print(f"hashes       k = {b.k} = ceil({-math.log2(p):.3f})")
    print(f"array size   m = {b.m}")
    for i in range(n):
        b.add(i)
        assert i in b
    print(f"approx_items(): {int(b.approx_items())}")
    print(f"calculate_p(): {b.calculate_p():.5f}")

    N = 100000
    false_pos = sum(i in b for i in range(n, n + N))
    print(f"experimental : {false_pos / N:.5f}\n")


if __name__ == "__main__":
    bloom_filter_stats(5000, 0.05)
    bloom_filter_stats(10000, 0.01)
    bloom_filter_stats(50000, 0.005)
    bloom_filter_stats(100000, 0.002)
