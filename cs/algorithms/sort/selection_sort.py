from typing import TypeVar

from cs.util import Comparable

T = TypeVar("T", bound=Comparable)


def selection_sort(array: list[T]) -> list[T]:
    """
    Selection sort algorithm implementation.

    Runtime: O(n^2)
    """
    for i in range(len(array) - 1):
        least = i
        for k in range(i + 1, len(array)):
            if array[k] < array[least]:
                least = k
        if least != i:
            array[least], array[i] = array[i], array[least]
    return array
