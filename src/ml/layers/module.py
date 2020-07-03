from typing import Any, Dict, Tuple, Union

import numpy as np


class Module:
    def __init__(self) -> None:
        self.cache: Tuple[Any, ...] = ()

    def forward(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)

    def parameters(self, *layers: str) -> Dict[str, Any]:
        result = {}
        for layer_name in layers:
            if hasattr(self, layer_name):
                submodel = getattr(self, layer_name)
                result[layer_name] = (
                    submodel.parameters() if isinstance(submodel, Module) else submodel
                )
            else:
                raise ValueError(
                    f"Not a valid attribute of {self.__class__.__name__}: {layer_name} "
                )
        return result
