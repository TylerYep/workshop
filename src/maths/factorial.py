def factorial_iterative(n: int) -> int:
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    value = 1
    for i in range(1, n + 1):
        value *= i
    return value


def factorial_recursive(n: int) -> int:
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)
