from cs.maths.karatsuba import karatsuba


def test_karatsuba() -> None:
    assert karatsuba(15463, 23489) == 15463 * 23489
    assert karatsuba(3, 9) == 3 * 9
    assert karatsuba(254, 0) == 0
    assert karatsuba(1, 6546) == 6546
    assert karatsuba(-50, 50) == -2500
