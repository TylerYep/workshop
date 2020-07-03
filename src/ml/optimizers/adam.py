from typing import Any, Tuple

import numpy as np

from ..layers.module import Module
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
        model: Module,
        lr: float = 1e-3,
        betas: Tuple[float, float] = (0.9, 0.999),
        eps: float = 1e-08,
    ) -> None:
        super().__init__(model)
        self.lr = lr
        self.betas = betas
        self.eps = eps

        def init_context(w: np.ndarray) -> Tuple[Any, ...]:
            """ Initialize context using weights. """
            m = np.zeros_like(w)
            v = np.zeros_like(w)
            t = 0
            return m, v, t

        self.set_context(init_context)

    def _step(self, context: Tuple[Any, ...], w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        """
        w must have the same shape as params.

        For efficiency, update rules may perform in-place updates, mutating w and
        setting next_w equal to w.
        """
        (m, v, t) = context

        beta1, beta2 = self.betas
        m = beta1 * m + (1 - beta1) * dw
        v = beta2 * v + (1 - beta2) * (dw * dw)
        t += 1

        alpha = self.lr * np.sqrt(1 - beta2 ** t) / (1 - beta1 ** t)
        w -= alpha * (m / (np.sqrt(v) + self.eps))

        return w, (m, v, t)
