from __future__ import annotations

import random
from typing import TypeVar

import pytest

from cs.structures import Cuckoo, HashTable, LinearProbing, RobinHood
from cs.structures.hash_table.hash_table import KT, VT
from cs.util import Comparable

T = TypeVar("T", bound=Comparable)
parametrize_hash_table_type = pytest.mark.parametrize(
    "hash_table_type", ("Cuckoo", "LinearProbing", "RobinHood")
)


def construct_hash_table(hash_table_type: str, num_buckets: int) -> HashTable[KT, VT]:
    hash_table_map = {
        constructor.__name__: constructor
        for constructor in (Cuckoo, LinearProbing, RobinHood)
    }
    return hash_table_map[hash_table_type](num_buckets)


@parametrize_hash_table_type
class TestHashTable:
    @staticmethod
    @pytest.mark.parametrize("n", (1, 100))
    def test_insert_contains(hash_table_type: str, n: int) -> None:
        """ Test creating a hash_table and adding 100 values to it. """
        hash_table: HashTable[int, int] = construct_hash_table(hash_table_type, n)
        random_values = list(range(n))
        random.shuffle(random_values)
        for i in range(n):
            assert len(hash_table) == i
            random_value = random_values[i]
            hash_table.insert(random_value, random_value)
            assert random_value in hash_table

        with pytest.raises(KeyError):
            # Max capacity
            hash_table.insert(-2, -2)

    @staticmethod
    @pytest.mark.parametrize("n", (1, 100))
    def test_remove(hash_table_type: str, n: int) -> None:
        """ Test creating a hash_table and removing 100 values from it. """
        hash_table: HashTable[int, int] = construct_hash_table(hash_table_type, n)
        for i in range(n):
            hash_table.insert(i, i)

        random_values = list(range(n))
        random.shuffle(random_values)
        for i, key in enumerate(random_values):
            hash_table.remove(key)
            assert len(hash_table) == n - i - 1

    @staticmethod
    def test_accessors(hash_table_type: str) -> None:
        """ Test creating a hash_table and adding 100 values to it. """
        n = 10
        hash_table: HashTable[int, str] = construct_hash_table(hash_table_type, n)
        for i in range(n):
            hash_table[i] = f"hello {i}"

        assert hash_table[1] == "hello 1"
        del hash_table[1]
        with pytest.raises(KeyError):
            _ = hash_table[1]
