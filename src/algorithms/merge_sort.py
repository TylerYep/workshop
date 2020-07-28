from typing import List, TypeVar

from src.algorithms.util.comparable_type import Comparable

C = TypeVar("C", bound=Comparable)


def merge(left: List[C], right: List[C]) -> List[C]:
    """ Merge sort merging function. """
    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    return result


def merge_sort(array: List[C]) -> List[C]:
    """ Merge sort algorithm implementation. """
    if len(array) <= 1:
        return array

    half = len(array) // 2
    left = merge_sort(array[:half])
    right = merge_sort(array[half:])
    return merge(left, right)
