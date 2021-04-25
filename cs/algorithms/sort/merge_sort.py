from typing import TypeVar

from cs.util import Comparable

T = TypeVar("T", bound=Comparable)


def merge_sort(array: list[T]) -> list[T]:
    """
    Merge sort algorithm implementation.

    Runtime: O(n log n)
    """

    def merge(left: list[T], right: list[T]) -> list[T]:
        """Merge sort merging function."""
        left_index, right_index = 0, 0
        result = []
        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
        return result + left[left_index:] + right[right_index:]

    if len(array) <= 1:
        return array

    half = len(array) // 2
    left = merge_sort(array[:half])
    right = merge_sort(array[half:])
    return merge(left, right)
