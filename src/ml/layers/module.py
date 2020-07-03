from typing import Any, Dict, Tuple

import numpy as np


class Module:
    def __init__(self) -> None:
        self.cache: Tuple[Any, ...] = ()

    def forward(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.forward(x)

    def parameters(self, *layers: str) -> Dict[str, Dict[str, Any]]:
        result = {}
        for submodel_name in layers:
            if hasattr(self, submodel_name):  # Guaranteed
                submodel = getattr(self, submodel_name)
                if isinstance(submodel, Module):
                    result[submodel_name] = submodel.parameters()
                else:
                    result[submodel_name] = {}
            else:
                raise ValueError(
                    f"Not a valid attribute of {self.__class__.__name__}: {submodel_name} "
                )
        return result
