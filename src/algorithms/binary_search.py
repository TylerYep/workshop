from typing import List, TypeVar

from src.algorithms.sort.comparable import Comparable

C = TypeVar("C", bound=Comparable)


def binary_search(arr: List[C], target: C) -> int:
    """ Returns the index of target element, or -1 if it cannot be found. """
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


def left_right_binary_search(arr: List[C], target: C, is_left: bool = True) -> int:
    """
    Returns the leftmost index of target element, or -1 if it cannot be found.
    Returns rightmost index if is_left is False.
    Allows duplicates.
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
