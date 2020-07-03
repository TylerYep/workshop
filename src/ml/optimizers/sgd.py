from typing import Any, Tuple

import numpy as np

from ..layers.module import Module
from .optimizer import Optimizer


class SGD(Optimizer):
    """
    Performs vanilla stochastic gradient descent.
    """

    def __init__(self, model: Module, lr: float = 1e-2) -> None:
        super().__init__(model)
        self.lr = lr

    def _step(self, context: Tuple[Any, ...], w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        del context

        w -= self.lr * dw

        return w
