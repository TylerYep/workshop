import timeit
from dataclasses import dataclass


def test(a):
    if a == "a":

        @dataclass(repr=False)
        class A:
            x: int = 4
            y: str = "yooo"

            def __repr__(self) -> str:
                return self.y

        return A()
    if a == "b":

        @dataclass
        class B:
            x: int = 4
            y: str = "yooo"

            def __repr__(self) -> str:
                return self.y

        return B()
    if a == "c":

        @dataclass(repr=False)
        class C:
            x: int = 4
            y: str = "yooo"

        return C()
    if a == "d":

        @dataclass(repr=False)
        class D:
            x: int = 4
            y: str = "yooo"

        return D()
    if a == "e":

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
