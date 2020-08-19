from src.algorithms import quick_select


def test_quick_select() -> None:
    assert quick_select([2, 4, 5, 7, 899, 54, 32], 5) == 54
    assert quick_select([2, 4, 5, 7, 899, 54, 32], 1) == 4
    assert quick_select([5, 4, 3, 2], 2) == 4
    assert quick_select([3, 5, 7, 10, 2, 12], 3) == 7
