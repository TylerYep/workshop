from typing import List, TypeVar

from src.algorithms.sort.comparable import Comparable

C = TypeVar("C", bound=Comparable)


def selection_sort(array: List[C]) -> List[C]:
    """ Selection sort algorithm implementation. """
    for i in range(len(array) - 1):
        least = i
        for k in range(i + 1, len(array)):
            if array[k] < array[least]:
                least = k
        if least != i:
            array[least], array[i] = array[i], array[least]
    return array
