from __future__ import annotations

import pytest

from cs.util import idempotent


@idempotent
def func(x: list[int]) -> None:
    if not x:  # comment this line to verify the test
        x += [9]


@pytest.mark.test_idempotency
def test_func() -> None:
    x: list[int] = []

    func(x)

    assert x == [9]


def test_func_2() -> None:
    x: list[int] = []

    assert not x


@pytest.mark.test_idempotency
class TestStuff:
    @staticmethod
    def test_func() -> None:
        x: list[int] = []

        func(x)

        assert x == [9]

    @staticmethod
    def test_func_2() -> None:
        x: list[int] = []

        assert not x
