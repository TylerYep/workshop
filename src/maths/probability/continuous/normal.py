import math
from dataclasses import dataclass

from src.maths.probability.rv import RandomVariable


@dataclass
class Normal(RandomVariable):
    """
    The normal distribution is a type of continuous probability distribution
    for a real-valued random variable.

    https://en.wikipedia.org/wiki/Normal_distribution
    """

    mu: float = 0
    sigma: float = 1

    def __post_init__(self) -> None:
        self.sigma_sq = self.sigma ** 2

    def __str__(self) -> str:
        return f"Normal(μ={self.mu}, σ²={self.sigma_sq})"

    def pdf(self, x: float) -> float:
        return (
            1
            / math.sqrt(2 * math.pi * self.sigma_sq)
            * math.exp(-((x - self.mu) ** 2) / (2 * self.sigma_sq))
        )

    def cdf(self, x: float) -> float:
        return 0
