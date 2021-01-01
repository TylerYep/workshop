def greatest_common_divisor(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def least_common_multiple(a: int, b: int) -> int:
    return a // greatest_common_divisor(a, b) * b
