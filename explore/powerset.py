import itertools
import timeit


def itertools_magic(nums):
    return list(
        itertools.chain.from_iterable(itertools.combinations(nums, r) for r in nums)
    )


def sum_magic(nums):
    return sum((list(itertools.combinations(nums, r)) for r in nums), [])


def comprehension(nums):
    return [
        item
        for sublist in (itertools.combinations(nums, r) for r in nums)
        for item in sublist
    ]


NUM = 10000
numbers = range(1, 6)
result = timeit.timeit(lambda: itertools_magic(numbers), number=NUM)
print(result)
result = timeit.timeit(lambda: sum_magic(numbers), number=NUM)
print(result)
result = timeit.timeit(lambda: comprehension(numbers), number=NUM)
print(result)

output = itertools_magic(numbers)
print(output)
print(len(output))

assert itertools_magic(numbers) == sum_magic(numbers) == comprehension(numbers)
