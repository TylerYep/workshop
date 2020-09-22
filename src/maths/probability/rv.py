from __future__ import annotations


class RandomVariable:

    # def __add__(self, other: object) -> RandomVariable:
    #     if isinstance(other, RandomVariable):
    #         result = RandomVariable()
    #         result.pdf = lambda x: self.pdf(x) + other.pdf(x)
    #         return result
    #     raise TypeError

    def pdf(self, x: float) -> float:
        raise NotImplementedError

    def cdf(self, x: float) -> float:
        raise NotImplementedError
