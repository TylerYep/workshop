"""
See docs/karatsuba.md for code credits and implementation details.
Author: Keith Schwarz (htiek@cs.stanford.edu)
"""


def add(lhs: list[int], rhs: list[int], base: int) -> list[int]:
    """
    Adds two arbitrary-precision values in some base together.

    Given two arrays lhs and rhs of digits in some base 'base,' returns an
    array of the number lhs + rhs encoded in base 'base.'
    """

    # Pad the two inputs to be the same length.
    length = max(len(lhs), len(rhs))
    lhs = [0] * (length - len(lhs)) + lhs
    rhs = [0] * (length - len(rhs)) + rhs

    # Track the carry from the previous column; initially this is zero.
    carry = 0

    # Track the result.  We'll build the array up in reverse to avoid costly
    # prepend operations that aren't relevant.
    result = []

    # Iterate across the digits in reverse, computing the sum.
    for i in range(1, len(lhs) + 1):
        # Sum the carry and the two values in this column
        column = lhs[-i] + rhs[-i] + carry

        # Output the column value (after modding by the base)
        result.append(column % base)

        # Update the carry
        carry = column // base

    # Prepend the carry to the result if it's nonzero.
    if carry != 0:
        result.append(carry)

    # Reverse the order of the resulting digits; that's the more proper way
    # to hand them back.
    result.reverse()

    return result


def subtract(lhs: list[int], rhs: list[int], base: int) -> list[int]:
    """
    Subtracts two arbitrary-precision values in some base.

    Given two arrays lhs and rhs of digits in some base 'base,' returns an
    array of the number lhs - rhs encoded in base 'base.'  It is assumed that
    lhs >= rhs; an error occurs if this is not the case.
    """

    # Pad the two inputs to be the same length.
    length = max(len(lhs), len(rhs))
    lhs = [0] * (length - len(lhs)) + lhs
    rhs = [0] * (length - len(rhs)) + rhs

    # Track the result.  We'll build the array up in reverse to avoid costly
    # prepend operations that aren't relevant.
    result = []

    # Iterate across the digits in reverse, subtracting the values.
    for i in range(1, len(lhs) + 1):
        # Compute the difference in this column.
        difference = lhs[-i] - rhs[-i]

        # If we can subtract without borrowing, do so.
        if difference >= 0:
            result.append(difference)
            continue

        # Otherwise, we have to borrow from previous columns.
        for j in range(i + 1, length + 1):
            # Drop the value of this digit by one.  We do this by adding
            # base - 1 and then modding by base, which is equivalent to
            # subtracting one modulo base.
            lhs[-j] = (lhs[-j] + (base - 1)) % base

            # If this value didn't wrap around (i.e. its value is not
            # base - 1), then we're done.  Otherwise, we have to go to the
            # previous digit.
            if lhs[-j] != base - 1:
                break

        # Finally, update the result by appending the correct value.
        # Since we just computed lhs - rhs, we actually want to compute
        # (base + lhs) - rhs.
        result.append(difference + base)

    # Reverse the order of the resulting digits; that's the more proper way
    # to hand them back.
    result.reverse()

    return result


def multiply(lhs: list[int], rhs: list[int], base: int) -> list[int]:
    """
    Multiplies two arbitrary-precision values in some base.

    Given two arrays of lhs and rhs of digits in some base 'base,' returns
    an array of digits corresponding to their product using the Karatsuba
    algorithm.
    """
    assert len(lhs) > 0
    assert len(rhs) > 0

    # Pad the two inputs to be the same length.
    length = max(len(lhs), len(rhs))
    lhs = [0] * (length - len(lhs)) + lhs
    rhs = [0] * (length - len(rhs)) + rhs

    # If the numbers are one digit each, just multiply them and convert the
    # answer back to an (up to) two digit number.
    if length == 1:
        # Compute the true answer.
        result = lhs[0] * rhs[0]

        # Convert it back to an array.
        return [result] if result < base else [result // base, result % base]

    # Otherwise, we need to use Karatsuba's recursive algorithm to compute the
    # values.  To do this, we'll first compute how many digits we'll put into
    # each of the smaller numbers.  This is given by ceil(length / 2), which
    # can be represented beautifully by computing (length + 1) / 2.  This
    # works because if length is even (length + 1) / 2 = (2n + 1) / 2 = n
    # when using integer division, and if length is odd (length + 1) / 2 =
    # (2n + 1 + 1) / 2 = (2n + 2) / 2 = n + 1.
    m0 = (length + 1) // 2
    m1 = length // 2

    # Split the inputs in half.
    x0, x1 = lhs[:m0], lhs[m0:]
    y0, y1 = rhs[:m0], rhs[m0:]

    # Compute p0, p1, and p2.
    p0 = multiply(x0, y0, base)
    p1 = multiply(add(x0, x1, base), add(y0, y1, base), base)
    p2 = multiply(x1, y1, base)

    # Since z0 = p0 and z2 = p2, we don't need to compute them.  However, we
    # do need to compute z1 = p1 - p0 - p2.
    z0 = p0
    z1 = subtract(p1, add(p0, p2, base), base)
    z2 = p2

    # From these results, compute z0 b^(2m) + z1 b^m + z2.  We separate out
    # each of these operations.
    z0prod = z0 + [0] * (2 * m1)
    z1prod = z1 + [0] * m1
    z2prod = z2

    return add(add(z0prod, z1prod, base), z2prod, base)


def karatsuba(a: int, b: int) -> int:
    """
    Alternative karatsuba implementation for integers instead of lists.
    This is similar to the actual Python implempentation of multiplication.
    """
    len_a, len_b = len(str(a)), len(str(b))
    if len_a == 1 or len_b == 1:
        return a * b

    m1 = max(len_a, len_b)
    m2 = m1 // 2

    a1, a2 = divmod(a, 10**m2)
    b1, b2 = divmod(b, 10**m2)

    x = karatsuba(a2, b2)
    y = karatsuba(a1 + a2, b1 + b2)
    z = karatsuba(a1, b1)

    result = (z * 10 ** (2 * m2)) + ((y - z - x) * 10**m2) + x
    return int(result)
