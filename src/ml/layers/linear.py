from typing import Any, Dict

import numpy as np

from .module import Module


class Linear(Module):
    def __init__(self, input_dim: int, output_dim: int, bias: bool = True) -> None:
        super().__init__()
        del bias
        self.w = np.random.normal(scale=1e-3, size=(input_dim, output_dim))
        self.b = np.zeros(output_dim)

    def parameters(self, *layers: str) -> Dict[str, Dict[str, Any]]:
        """
        This function returns the parameters of the model that need gradients,
        in the order that they are returned in backward().
        """
        del layers
        return super().parameters("w", "b")

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Computes the forward pass for an affine (fully-connected) layer.

        The input x has shape (N, d_1, ..., d_k) where x[i] is the ith input.
        We multiply this against a weight matrix of shape (D, M) where
        D = prod_i d_i

        Inputs:
        x - Input data, of shape (N, d_1, ..., d_k)
        w - Weights, of shape (D, M)
        b - Biases, of shape (M,)

        Returns a tuple of:
        - out: output, of shape (N, M)
        - cache: (x, w, b)
        """
        out = x.reshape(x.shape[0], -1).dot(self.w) + self.b
        self.cache = (x,)
        return out

    def backward(self, dout: np.ndarray) -> np.ndarray:
        """
        Computes the backward pass for an affine layer.

        Inputs:
        - dout: Upstream derivative, of shape (N, M)
        - cache: Tuple of:
        - x: Input data, of shape (N, d_1, ... d_k)
        - w: Weights, of shape (D, M)

        Returns a tuple of:
        - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
        - dw: Gradient with respect to w, of shape (D, M)
        - db: Gradient with respect to b, of shape (M,)
        """
        (x,) = self.cache
        dx = dout.dot(self.w.T).reshape(x.shape)
        dw = x.reshape(x.shape[0], -1).T.dot(dout)
        db = np.sum(dout, axis=0)
        return dx, dw, db
