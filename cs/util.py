import dataclasses
import os
import random
from abc import abstractmethod
from typing import Any, Protocol, TypeVar

import prettyprinter
from prettyprinter.prettyprinter import IMPLICIT_MODULES

C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


# TODO: Make this not return a module, fix the WolfBot version as well.
def init_prettyprinter() -> Any:
    """ Initialize prettyprinter and add all IMPLICIT_MODULES. """
    prettyprinter.install_extras(include={"python"})
    prettyprinter.register_pretty(predicate=dataclasses.is_dataclass)(
        pretty_dataclass_instance
    )
    for root, _, files in os.walk("cs"):
        for filename in files:
            if filename.endswith(".py") and "__" not in filename:
                module_name = os.path.splitext(filename)[0]
                prefix = ".".join(root.split(os.sep) + [module_name])
                IMPLICIT_MODULES.add(prefix)
    return prettyprinter


def pretty_dataclass_instance(value: Any, ctx: Any) -> Any:
    cls = type(value)
    field_defs = dataclasses.fields(value)

    kwargs = {}
    for field_def in field_defs:
        # repr is True by default, therefore if this if False, the user
        # has explicitly indicated they don't want to display the field value.
        if not field_def.repr:
            continue

        default = field_def.default
        default_factory = field_def.default_factory  # type: ignore
        true_val = getattr(value, field_def.name)
        display_attr = (
            default is default_factory is dataclasses.MISSING  # type: ignore
            or (default is not dataclasses.MISSING and default != true_val)
            or (
                default_factory is not dataclasses.MISSING  # type: ignore
                and default_factory() != true_val
            )
        )
        if display_attr:
            kwargs[field_def.name] = true_val

    if hasattr(value, "kwargs"):
        kwargs |= value.kwargs

    return prettyprinter.pretty_call(ctx, cls, **kwargs)


def weighted_coin_flip(prob: float) -> bool:
    """ Returns True with probability prob. """
    return random.choices([True, False], [prob, 1 - prob])[0]


formatter = init_prettyprinter()
