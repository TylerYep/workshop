import numpy as np

from .optimizer import Optimizer


class RMSProp(Optimizer):
    """
    Uses the RMSProp update rule, which uses a moving average of squared
    gradient values to set adaptive per-parameter learning rates.

    config format:
    - learning_rate: Scalar learning rate.
    - decay_rate: Scalar between 0 and 1 giving the decay rate for the squared
        gradient cache.
    - epsilon: Small scalar used for smoothing to avoid dividing by zero.
    - cache: Moving average of second moments of gradients.
    """

    def __init__(
        self, w: np.ndarray, lr: float = 1e-2, decay_rate: float = 0.99, eps: float = 1e-8
    ) -> None:
        self.lr = lr
        self.decay_rate = decay_rate
        self.eps = eps
        self.v = np.zeros_like(w)

    def _step(self, w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        self.v = self.decay_rate * self.v + (1 - self.decay_rate) * dw ** 2
        w -= self.lr * dw / (np.sqrt(self.v) + self.eps)
        return w
