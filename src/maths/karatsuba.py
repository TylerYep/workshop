def karatsuba(a: int, b: int) -> int:
    """
    This is similar to the actual Python implempentation of multiplication.
    """
    len_a, len_b = len(str(a)), len(str(b))
    if len_a == 1 or len_b == 1:
        return a * b

    m1 = max(len_a, len_b)
    m2 = m1 // 2

    a1, a2 = divmod(a, 10 ** m2)
    b1, b2 = divmod(b, 10 ** m2)

    x = karatsuba(a2, b2)
    y = karatsuba(a1 + a2, b1 + b2)
    z = karatsuba(a1, b1)

    result = (z * 10 ** (2 * m2)) + ((y - z - x) * 10 ** m2) + x
    return int(result)
