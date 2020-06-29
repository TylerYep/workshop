import time

def timed(f):
    start = time.perf_counter()
    for _ in range(100):
        f(10000)
    end = time.perf_counter()
    return end - start

def append_loop(n):
    """Simple loop with append"""
    my_list = []
    for i in range(n):
        my_list.append(0)


def add_loop(n):
    """Simple loop with +="""
    my_list = []
    for i in range(n):
        my_list += [0]


def list_comprehension(n):
    """List comprehension"""
    my_list = [0 for i in range(n)]


def integer_multiplication(n):
    """List and integer multiplication"""
    my_list = [0] * n

import numpy as np

def numpy_array(n):
    my_list = np.zeros(n)

print([timed(f) for f in [
    append_loop, add_loop, list_comprehension, integer_multiplication, numpy_array
]])
