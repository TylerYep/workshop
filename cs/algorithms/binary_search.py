from collections.abc import Sequence
from typing import TypeVar

from cs.util import Comparable

T = TypeVar("T", bound=Comparable)


def binary_search(arr: Sequence[T], target: T) -> int:
    """
    Returns the index of target element, or -1 if it cannot be found.
    Performs a left binary search, which is equivalent to:
        bisect.bisect_left(arr, target)

    Runtime: O(log n)
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        mid_val = arr[mid]
        if target == mid_val:
            return mid
        if mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def left_right_binary_search(arr: Sequence[T], target: T, is_left: bool = True) -> int:
    """
    Returns the leftmost index of target element, or -1 if it cannot be found.
    Returns rightmost index if is_left is False. Allows duplicates.
    Equivalent to:
        bisect.bisect_left(arr, target)
        bisect.bisect_right(arr, target) - 1

    Runtime: O(log n)
    """
    left = 0
    right = len(arr) - 1
    index = -1
    while left <= right:
        mid = left + (right - left) // 2
        mid_val = arr[mid]
        if mid_val == target:
            index = mid
            if is_left:
                right = mid - 1
            else:
                left = mid + 1
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    return index


def linear_search(arr: Sequence[T], target: T) -> int:
    """
    Returns the index of target element, or -1 if it cannot be found.

    Runtime: O(n)
    """
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1


def binary_search_recursive(arr: Sequence[T], target: T) -> int:
    if not arr:
        return -1
    midpoint = len(arr) // 2
    if arr[midpoint] == target:
        return midpoint
    if target < arr[midpoint]:
        return binary_search(arr[:midpoint], target)
    return binary_search(arr[midpoint + 1 :], target)
