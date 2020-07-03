import numpy as np

from .optimizer import Optimizer


class SGDMomentum(Optimizer):
    """
    Performs stochastic gradient descent with momentum.

    config format:
    - learning_rate: Scalar learning rate.
    - momentum: Scalar between 0 and 1 giving the momentum value.
        Setting momentum = 0 reduces to sgd.
    - velocity: A numpy array of the same shape as w and dw used to store a
        moving average of the gradients.
    """

    def __init__(self, w: np.ndarray, lr: float = 1e-2, momentum: float = 0.9) -> None:
        self.lr = lr
        self.b = momentum
        self.v = np.zeros_like(w)

    def _step(self, w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        self.v = self.b * self.v - self.lr * dw
        w += self.v
        return w
