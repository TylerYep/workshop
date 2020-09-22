from dataclasses import dataclass

from src.maths.probability.rv import RandomVariable


@dataclass
class Uniform(RandomVariable):
    a: int = 0
    b: int = 1

    def pdf(self, x: float) -> float:
        if self.a <= x <= self.b:
            return 1 / (self.b - self.a)
        return 0

    def cdf(self, x: float) -> float:
        if x < self.a:
            return 0
        if x > self.b:
            return 1
        return (x - self.a) / (self.b - self.a)

    def expectation(self) -> float:
        return 0.5 * (self.a + self.b)

    def variance(self) -> float:
        return ((self.b - self.a) ** 2) / 12


# u = Uniform()
# v = Uniform()
# assert E(u + v) == 1

# create add operators for random variables
# return a Sum object with a custom expectation and variance?
