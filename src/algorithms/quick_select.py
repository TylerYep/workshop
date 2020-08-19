import random
from typing import List, Sequence, Tuple, TypeVar

from src.algorithms.sort.comparable import Comparable

C = TypeVar("C", bound=Comparable)


def quick_select(items: Sequence[C], index: int) -> C:
    """
    A Python implementation of the quick select algorithm, which is efficient for
    calculating the value that would appear in the index of a list if it would be
    sorted, even if it is not already sorted.
    """

    def _partition(data: Sequence[C], pivot: C) -> Tuple[List[C], List[C], List[C]]:
        """
        Three way partition the data into smaller, equal, and greater lists,
        in relation to the pivot
        :param data: Data to be sorted (list)
        :param pivot: Value to partition the data on
        :return: Three lists: smaller, equal and greater
        """
        less, equal, greater = [], [], []
        for element in data:
            if element < pivot:
                less.append(element)
            elif element > pivot:
                greater.append(element)
            else:
                equal.append(element)
        return less, equal, greater

    if index < 0 or index >= len(items):
        raise ValueError(f"Index {index} is out of range.")

    pivot = items[random.randrange(len(items))]
    smaller, equal, larger = _partition(items, pivot)
    m = len(smaller)  # end of smaller
    n = m + len(equal)  # start of larger

    # index is the pivot
    if m <= index < n:
        return pivot
    # must be in smaller
    if index < m:
        return quick_select(smaller, index)
    # must be in larger
    return quick_select(larger, index - n)
