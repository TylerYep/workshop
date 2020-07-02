import numpy as np


class SGD:
    """
    Performs vanilla stochastic gradient descent.
    """

    def __init__(self, w: np.ndarray, lr: float = 1e-2) -> None:
        del w
        self.lr = lr

    def step(self, w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        w -= self.lr * dw
        return w
