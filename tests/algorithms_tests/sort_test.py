from typing import Any, List, Tuple

from src.algorithms.sort import bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort


def test_sort() -> None:
    sort_fns = (bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort)
    arrays: Tuple[List[Any], ...] = (
        [0, 5, 2, 3, 2],
        [],
        [-2, -45, -5],
        [-23, 0, 6, -4, 27, 34],
        ["low", "high", "you", "dragon", "flying"],
        list(range(10, 0, -1)),
    )

    for sort_fn in sort_fns:
        for array in arrays:
            assert sort_fn(list(array)) == sorted(array)
