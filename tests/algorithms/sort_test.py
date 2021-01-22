from typing import Any, Tuple

from cs.algorithms import (
    bubble_sort,
    bucket_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    selection_sort,
)


def test_sort() -> None:
    sort_fns = (bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort)
    arrays: Tuple[list[Any], ...] = (
        [0, 5, 2, 3, 2],
        [],
        [-2, -45, -5],
        [-23.5, 0.1, 6.4, -4.6, 27.9, 34.11, 0, 34.1],
        ["low", "high", "you", "dragon", "flying"],
        list(range(10, 0, -1)),
    )

    for sort_fn in sort_fns:
        for array in arrays:
            assert sort_fn(list(array)) == sorted(array)


def test_positive_int_sort() -> None:
    sort_fns = (bucket_sort, radix_sort)
    arrays: Tuple[list[int], ...] = (
        [0, 5, 2, 3, 2],
        [],
        list(range(10, 0, -1)),
    )

    for sort_fn in sort_fns:
        for array in arrays:
            assert sort_fn(list(array)) == sorted(array)
