import bisect

from cs.algorithms import binary_search, left_right_binary_search, linear_search
from tests.conftest import assert_a_faster_than_b


def test_binary_search() -> None:
    arr = range(1, 10)
    assert binary_search([0], target=0) == 0
    assert binary_search(range(10), target=1) == 1
    assert binary_search(arr, target=5) == 4
    assert binary_search(arr, target=8) == 7
    assert binary_search(arr, target=8) == bisect.bisect_left(arr, 8)

    UPPER_BOUND = 800
    nums = list(range(0, UPPER_BOUND, 2))
    for x in range(0, UPPER_BOUND, 4):
        assert binary_search(nums, target=x) == x // 2

    assert binary_search([1, 2, 4, 5, 6, 7, 8], target=3) == -1
    assert binary_search(nums, target=UPPER_BOUND + 1) == -1


def test_left_right_binary_search() -> None:
    arr = [0, 1, 2, 3, 3, 3, 6, 7, 8]
    assert left_right_binary_search([0], target=0) == 0
    assert left_right_binary_search(arr, target=3) == 3
    assert left_right_binary_search([5] * 20, target=5) == 0
    assert left_right_binary_search(range(10), target=8) == bisect.bisect_left(
        range(10), 8
    )

    assert left_right_binary_search([0], target=0, is_left=False) == 0
    assert left_right_binary_search([5] * 20, target=5, is_left=False) == 19
    assert left_right_binary_search(arr, target=3, is_left=False) == 5
    assert (
        left_right_binary_search(arr, target=3, is_left=False)
        == bisect.bisect_right(arr, 3) - 1
    )
    assert (
        left_right_binary_search(range(10), target=8, is_left=False)
        == bisect.bisect_right(range(10), 8) - 1
    )


def test_binary_search_runtime() -> None:
    lst = range(1501)
    assert_a_faster_than_b(binary_search, linear_search, lst, target=1500)
