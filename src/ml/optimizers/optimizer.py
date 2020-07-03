from typing import Dict

import numpy as np

from ..layers.module import Module


class Optimizer:

    # def __init__(self) -> None:
    #     # Store model here?
    #     pass

    def _step(self, w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def step(self, model: Module, gradients: Dict[str, np.ndarray]) -> None:
        for param_name, param_dict in model.parameters().items():
            real_param = getattr(model, param_name)
            if param_dict:
                self.step(real_param, gradients[param_name])

            elif hasattr(model, param_name):
                setattr(model, param_name, self._step(real_param, gradients[param_name]))
