from __future__ import annotations

import pytest

from cs.util import idempotent


@idempotent(equal_return=True)
def func(x: list[int]) -> None:
    if not x:  # comment this line to verify the test
        x += [9]
        # return True  # comment this line to verify the test


@pytest.mark.idempotent
def test_func() -> None:
    x: list[int] = []

    func(x)

    assert x == [9]


@pytest.mark.idempotent(run_twice=False)  # comment this line to verify the test
def test_func_2() -> None:
    x: list[int] = []

    func(x)

    assert x == [9]


@pytest.mark.idempotent(run_twice=True)
class TestIdempotency:
    @staticmethod
    def test_func() -> None:
        x: list[int] = []

        func(x)

        assert x == [9]

    @staticmethod
    def test_func_2() -> None:
        x: list[int] = []

        assert not x
