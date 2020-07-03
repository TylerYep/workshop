from typing import Tuple

import numpy as np

from .optimizer import Optimizer


class Adam(Optimizer):
    """
    Uses the Adam update rule, which incorporates moving averages of both the
    gradient and its square and a bias correction term.

    - lr: Scalar learning rate.
    - betas: Decay rate for moving average of first & second moment of gradient.
    - eps: Small scalar used for smoothing to avoid dividing by zero.
    - m: Moving average of gradient.
    - v: Moving average of squared gradient. (velocity)
    - t: Iteration number.
    """

    def __init__(
        self,
        w: np.ndarray,
        lr: float = 1e-3,
        betas: Tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-08,
    ) -> None:
        self.lr = lr
        self.betas = betas
        self.eps = eps

        self.m = np.zeros_like(w)
        self.v = np.zeros_like(w)
        self.t = 0

    def _step(self, w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        """
        w must have the same shape as params.

        For efficiency, update rules may perform in-place updates, mutating w and
        setting next_w equal to w.
        """
        beta1, beta2 = self.betas
        self.m = beta1 * self.m + (1 - beta1) * dw
        self.v = beta2 * self.v + (1 - beta2) * (dw * dw)
        self.t += 1

        alpha = self.lr * np.sqrt(1 - beta2 ** self.t) / (1 - beta1 ** self.t)
        w -= alpha * (self.m / (np.sqrt(self.v) + self.eps))
        return w
