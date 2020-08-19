# type: ignore
import time

import numpy as np


def timed(f):
    start = time.perf_counter()
    for _ in range(100):
        f(10000)
    end = time.perf_counter()
    return end - start


def append_loop(n):
    """Simple loop with append"""
    my_list = []
    for _ in range(n):
        my_list.append(0)


def add_loop(n):
    """Simple loop with +="""
    my_list = []
    for _ in range(n):
        my_list += [0]


def list_comprehension(n):
    """List comprehension"""
    _ = [0 for _ in range(n)]


def integer_multiplication(n):
    """List and integer multiplication"""
    _ = [0] * n


def numpy_array(n):
    _ = np.zeros(n)


fns = [append_loop, add_loop, list_comprehension, integer_multiplication, numpy_array]
print([timed(f) for f in fns])
