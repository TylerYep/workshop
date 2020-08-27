import timeit
from collections import Counter, defaultdict


def test(fruit_set):
    _ = dict(Counter(fruit_set))


def test2(fruit_set):
    counts = {}
    for fruit in fruit_set:
        if fruit in counts:
            counts[fruit] += 1
        else:
            counts[fruit] = 1


def test3(fruit_set):
    counts = defaultdict(int)
    for fruit in fruit_set:
        counts[fruit] += 1


def test4(fruit_set):
    if len(fruit_set) < 40:
        counts = {}
        for fruit in fruit_set:
            if fruit in counts:
                counts[fruit] += 1
            else:
                counts[fruit] = 1

    return dict(Counter(fruit_set))


if __name__ == "__main__":
    FRUITS = ("Apple", "Orange", "Grape", "Banana", "Banana", "Watermelon", "Lemon", "Peach") * 2
    print(len(FRUITS))
    y = timeit.timeit(lambda: test(FRUITS))
    print(y)
    y = timeit.timeit(lambda: test2(FRUITS))
    print(y)
    y = timeit.timeit(lambda: test3(FRUITS))
    print(y)
    y = timeit.timeit(lambda: test4(FRUITS))
    print(y)
