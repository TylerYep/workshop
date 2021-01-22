import random
from collections.abc import Sequence
from typing import TypeVar

from cs.util import Comparable

T = TypeVar("T", bound=Comparable)


def quick_select(items: Sequence[T], index: int) -> T:
    """
    A Python implementation of the quick select algorithm (also called the kth order
    statistic), which is efficient for calculating the value that would appear in the
    index of a list if it would be sorted, even if it is not already sorted.

    Partition the data into smaller and greater lists in relation to the pivot, then
    recurse.

    Average runtime: O(n)
    Runtime: O(n^2)
    This algorithm is often much better than sorting, which is O(n log n).
    """
    if index < 0 or index >= len(items):
        raise ValueError(f"Index {index} is out of range.")

    pivot = random.choice(items)
    equal, smaller, larger = 0, [], []
    for elem in items:
        if elem == pivot:
            equal += 1
        elif elem < pivot:
            smaller.append(elem)
        else:
            larger.append(elem)

    m = len(smaller)
    if index == m:
        return pivot
    if index < m:
        return quick_select(smaller, index)
    # eliminate all smaller elements than pivot
    return quick_select(larger, index - (m + equal))
