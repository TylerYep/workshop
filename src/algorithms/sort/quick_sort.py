from typing import List, TypeVar

from src.algorithms.sort.comparable import Comparable

C = TypeVar("C", bound=Comparable)


def quick_sort(array: List[C]) -> List[C]:
    """ Quick sort algorithm implementation. """
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
