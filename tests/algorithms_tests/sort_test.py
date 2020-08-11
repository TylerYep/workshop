from typing import Any, List, Tuple

from src.algorithms import (
    bubble_sort,
    bucket_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
    selection_sort,
    topological_sort,
)
from src.structures import Graph


def test_sort() -> None:
    sort_fns = (bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort)
    arrays: Tuple[List[Any], ...] = (
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
    arrays: Tuple[List[int], ...] = (
        [0, 5, 2, 3, 2],
        [],
        list(range(10, 0, -1)),
    )

    for sort_fn in sort_fns:
        for array in arrays:
            assert sort_fn(list(array)) == sorted(array)


def test_topological_sort() -> None:
    """
    Ordered from bottom to top
        a
       / \
      b   c
     / \
    d   e
    """
    graph: Graph[str, None] = Graph.from_iterable(
        {"a": ["c", "b"], "b": ["d", "e"], "c": [], "d": [], "e": []}
    )

    assert topological_sort(graph, "a") == ["c", "d", "e", "b", "a"]
