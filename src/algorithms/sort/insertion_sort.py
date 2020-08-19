from typing import List, TypeVar

from src.algorithms.sort.comparable import Comparable

C = TypeVar("C", bound=Comparable)


def insertion_sort(array: List[C]) -> List[C]:
    """
    Insertion sort algorithm implementation.

    Runtime: O(n^2)
    """
    for i in range(1, len(array)):
        j = i
        while j > 0 and array[j - 1] > array[j]:
            array[j], array[j - 1] = array[j - 1], array[j]
            j -= 1

    return array
