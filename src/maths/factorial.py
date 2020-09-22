def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    value = 1
    for i in range(1, n + 1):
        value *= i
    return value
