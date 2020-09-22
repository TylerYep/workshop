from src.maths.fibonacci import (
    fibonacci_formula,
    fibonacci_iterative,
    fibonacci_recursive,
)


def test_fibonacci() -> None:
    functions = [fibonacci_formula, fibonacci_iterative, fibonacci_recursive]
    answer = {}
    for fib in functions:
        answer[fib] = fib(100)
    assert answer[fibonacci_iterative][:12] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert answer[fibonacci_iterative] == answer[fibonacci_recursive]
    assert answer[fibonacci_iterative][:72] == answer[fibonacci_formula][:72]
