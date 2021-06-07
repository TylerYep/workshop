import timeit
from dataclasses import dataclass

from dataslots import dataslots  # type: ignore[import]


def test(a):
    if a == "a":

        @dataslots
        @dataclass(repr=False)
        class A:
            x: int = 4
            y: str = "yooo"

            def __repr__(self):
                return self.y

        return A()
    if a == "b":

        @dataslots
        @dataclass
        class B:
            x: int = 4
            y: str = "yooo"

            def __repr__(self):
                return self.y

        return B()
    if a == "c":

        @dataslots
        @dataclass(repr=False)
        class C:
            x: int = 4
            y: str = "yooo"

        return C()
    if a == "d":

        @dataslots
        @dataclass(repr=False)
        class D:
            x: int = 4
            y: str = "yooo"

        return D()
    if a == "e":

        @dataslots
        @dataclass(repr=False, eq=False, order=False)
        class E:
            x: int = 4
            y: str = "yooo"

        return E()
    return None


NUM = 10000
result = timeit.timeit(lambda: test("a"), number=NUM)
print(result)
result = timeit.timeit(lambda: test("b"), number=NUM)
print(result)
result = timeit.timeit(lambda: test("c"), number=NUM)
print(result)
result = timeit.timeit(lambda: test("d"), number=NUM)
print(result)
result = timeit.timeit(lambda: test("e"), number=NUM)
print(result)
