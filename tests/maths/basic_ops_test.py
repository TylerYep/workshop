from cs.maths.basic_ops import greatest_common_divisor, least_common_multiple


def test_gcd() -> None:
    assert greatest_common_divisor(24, 40) == 8
    assert greatest_common_divisor(1, 1) == 1
    assert greatest_common_divisor(1, 800) == 1
    assert greatest_common_divisor(11, 37) == 1
    assert greatest_common_divisor(3, 5) == 1
    assert greatest_common_divisor(16, 4) == 4
    assert greatest_common_divisor(24, 40) == 8


def test_lcm() -> None:
    assert least_common_multiple(5, 2) == 10
    assert least_common_multiple(12, 76) == 228
    assert least_common_multiple(10, 20) == 20
    assert least_common_multiple(13, 15) == 195
    assert least_common_multiple(4, 31) == 124
    assert least_common_multiple(10, 42) == 210
    assert least_common_multiple(43, 34) == 1462
    assert least_common_multiple(5, 12) == 60
    assert least_common_multiple(12, 25) == 300
    assert least_common_multiple(10, 25) == 50
    assert least_common_multiple(6, 9) == 18
