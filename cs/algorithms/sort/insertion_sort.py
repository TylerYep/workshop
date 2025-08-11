from cs.util import Comparable


def insertion_sort[T: Comparable](array: list[T]) -> list[T]:
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
