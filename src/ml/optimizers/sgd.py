import numpy as np

from .optimizer import Optimizer


class SGD(Optimizer):
    """
    Performs vanilla stochastic gradient descent.
    """

    def __init__(self, w: np.ndarray, lr: float = 1e-2) -> None:
        del w
        self.lr = lr

    def _step(self, w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        assert w.shape == dw.shape
        w -= self.lr * dw
        return w
