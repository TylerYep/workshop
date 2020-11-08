from typing import List, TypeVar

from src.util import Comparable

T = TypeVar("T", bound=Comparable)


def quick_sort(array: List[T]) -> List[T]:
    """
    Quick sort algorithm implementation.

    Runtime: O(n log n)
    """
    if len(array) <= 1:
        return array

    pivot = array.pop()
    greater, lesser = [], []
    for element in array:
        if element > pivot:
            greater.append(element)
        else:
            lesser.append(element)
    return quick_sort(lesser) + [pivot] + quick_sort(greater)
