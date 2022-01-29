import math


def fibonacci_recursive(n: int) -> list[int]:
    cache: dict[int, int] = {0: 0, 1: 1}

    def _fib(n: int) -> int:
        if n in cache:
            return cache[n]
        result = _fib(n - 1) + _fib(n - 2)
        cache[n] = result
        return result

    _ = _fib(n - 1)
    return list(cache.values())


def fibonacci_iterative(n: int) -> list[int]:
    seq_out = [0, 1]
    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
        seq_out.append(b)
    return seq_out


def fibonacci_formula(n: int) -> list[int]:
    """
    Uses Binet's formula to calculate the fibonacci sequence.
    This formula does not yield correct results past n = 72 because of rounding errors.
    """
    seq_out = [0, 1]
    sqrt_5 = math.sqrt(5)
    phi_1 = (1 + sqrt_5) / 2
    phi_2 = (1 - sqrt_5) / 2
    for i in range(2, n):
        temp_out = (phi_1**i - phi_2**i) / sqrt_5
        seq_out.append(int(temp_out))
    return seq_out
