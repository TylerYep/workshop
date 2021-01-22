from typing import TypeVar

from cs.util import Comparable

T = TypeVar("T", bound=Comparable)


def bubble_sort(array: list[T]) -> list[T]:
    """
    Bubble sort algorithm implementation.

    Runtime: O(n^2)
    """
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array
