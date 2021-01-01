from cs.algorithms import quick_select


def test_quick_select() -> None:
    assert quick_select([2, 4, 5, 7, 899, 54, 32], 5) == 54
    assert quick_select([2, 4, 5, 7, 899, 54, 32], 1) == 4
    assert quick_select([5, 4, 3, 2], 2) == 4
    assert quick_select([3, 5, 7, 10, 2, 12], 3) == 7

    assert quick_select([2, 1, 3, 4, 5], 2) == 3
    assert quick_select([2, 1, 3, 4, 5], 0) == 1
    assert quick_select([2, 1, 3, 4, 5], 4) == 5
    assert quick_select([3, 2, 5, 6, 7, 8], 1) == 3
    assert quick_select([25, 21, 98, 100, 76, 22, 43, 60, 89, 87], 3) == 43
