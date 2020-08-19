from typing import List, TypeVar

from src.algorithms.sort.comparable import Comparable

C = TypeVar("C", bound=Comparable)


def bubble_sort(array: List[C]) -> List[C]:
    """
    Bubble sort algorithm implementation.

    Runtime: O(n^2)
    """
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array
