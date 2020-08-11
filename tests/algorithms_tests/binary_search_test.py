from src.algorithms import binary_search, left_right_binary_search


def test_binary_search() -> None:
    assert binary_search([0], target=0) == 0
    assert binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8], target=1) == 1
    assert binary_search([1, 2, 4, 5, 6, 7, 8], target=3) == -1
    assert binary_search([1, 2, 3, 4, 5, 6, 7, 8], target=5) == 4
    assert binary_search([1, 2, 3, 4, 5, 6, 7, 8], target=8) == 7
    UPPER_BOUND = 800
    nums = list(range(0, UPPER_BOUND, 2))
    for x in range(0, UPPER_BOUND, 4):
        assert binary_search(nums, target=x) == x // 2
    assert binary_search(nums, target=UPPER_BOUND + 1) == -1


def test_left_right_binary_search() -> None:
    assert left_right_binary_search([0], target=0) == 0
    assert left_right_binary_search([0, 1, 2, 3, 3, 3, 6, 7, 8], target=3) == 3
    assert left_right_binary_search([5] * 20, target=5) == 0

    assert left_right_binary_search([0], target=0, is_left=False) == 0
    assert left_right_binary_search([0, 1, 2, 3, 3, 3, 6, 7, 8], target=3, is_left=False) == 5
    assert left_right_binary_search([5] * 20, target=5, is_left=False) == 19
