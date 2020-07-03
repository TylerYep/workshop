from typing import Any, Callable, Dict, Optional, Tuple, Union

import numpy as np

from ..layers.module import Module


class Optimizer:
    def __init__(self, model: Module) -> None:
        self.param_tree = model.parameters()

    def set_context(
        self,
        context_initializer: Callable[[np.ndarray], Tuple[Any, ...]],
        param_tree: Optional[Dict[str, Any]] = None,
    ) -> None:
        if param_tree is None:
            param_tree = self.param_tree

        for param_name, param in param_tree.items():
            if isinstance(param, dict):
                self.set_context(context_initializer, param)
            else:
                param_tree[param_name] = context_initializer(param)

    def _step(self, context: Tuple[Any, ...], w: np.ndarray, dw: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def step(
        self,
        model: Module,
        gradients: Dict[str, np.ndarray],
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Model parameters and gradients should be matching dictionaries.
        Traverse both dictionaries - on a branch, recurse on the branch.
        On a leaf, pass the context into the _step function.

        Parameter context should always be None from the user's perspective.
        """
        if context is None:
            context = self.param_tree

        for param_name, param in model.parameters().items():
            submodel = getattr(model, param_name)  # Either a submodel or a weight w
            step_context = context[param_name]
            grad = gradients[param_name]
            if isinstance(param, dict):
                self.step(submodel, grad, step_context)
            elif hasattr(model, param_name):
                # assert w.shape == dw.shape
                assert submodel.shape == grad.shape
                new_w, new_context = self._step(step_context, submodel, grad)
                setattr(model, param_name, new_w)
                context[param_name] = new_context
            else:
                raise ValueError(f"{model.__class__.__name__} has no attribute: {param_name}")
