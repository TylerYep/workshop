import hashlib
import math
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

from bitarray import bitarray

T = TypeVar("T")


@dataclass
class BloomFilter(Generic[T]):
    """
    Implementation of a Bloom filter. An instance is initialized by its capacity `n`
    and error rate `p`. The capacity `n` is how many elements can be stored while
    maintaining no more than `p` false positives.

    Code adapted from @ilanschnell's bitarray project.
    """

    n: int
    p: float = 0.01

    def __post_init__(self) -> None:
        if not 0 < self.p < 1:
            raise ValueError("Invalid value of p.")
        self.k = math.ceil(-math.log2(self.p))  # number of hash functions
        self.m = math.ceil(-self.n * math.log2(self.p) / math.log(2))  # size of array
        self.array = bitarray(self.m)
        self.array.setall(0)
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return any(self.array)

    def __contains__(self, key: T) -> bool:
        return all(self.array[i] for i in self._hashes(key))

    def __str__(self) -> str:
        return f"{self.__class__.__qualname__}({self.array.to01()})"

    def calculate_p(self) -> float:
        """
        Calculate the actual false positive error rate `p` from the number of hashes `k`
        and the size if the bitarray `m`. This is slightly different from the given `p`,
        because the integer value of `k` is being used.
        """
        return pow(1 - math.exp(-self.k * self.n / self.m), self.k)

    def approx_items(self) -> int:
        """Return the approximate number of items in the Bloom filter."""
        count = self.array.count()
        return 0 if count == 0 else int(-self.m / self.k * math.log(1 - count / self.m))

    def add(self, key: T) -> None:
        self.size += 1
        for i in self._hashes(key):
            self.array[i] = 1

    def _hashes(self, key: T) -> Iterator[int]:
        """
        Generate k different hashes, each of which maps a key to one of
        the m array positions with a uniform random distribution.
        """
        h = hashlib.new("md5")
        h.update(str(key).encode())
        x = int(h.hexdigest(), 16)
        for _ in range(self.k):
            if x < 1024 * self.m:
                h.update(b"x")
                x = int(h.hexdigest(), 16)
            x, y = divmod(x, self.m)
            yield y
