import dataclasses
import random
from abc import abstractmethod
from pathlib import Path
from typing import Any, Protocol, TypeVar

import prettyprinter  # type: ignore[import]
from prettyprinter.prettyprinter import IMPLICIT_MODULES  # type: ignore[import]

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


class Formatter:
    """Wrapper class for PrettyPrinter."""

    def __init__(self, prettyprinter_module: Any) -> None:
        self.pformat = prettyprinter_module.pformat
        self.pprint = prettyprinter_module.pprint


def init_prettyprinter() -> Formatter:
    """Initialize prettyprinter and add all IMPLICIT_MODULES."""
    prettyprinter.install_extras(include={"python"})
    prettyprinter.register_pretty(predicate=dataclasses.is_dataclass)(
        pretty_dataclass_instance
    )
    for filepath in Path("cs").rglob("*.py"):
        module_name = filepath.stem
        if "__" not in module_name:
            prefix = ".".join(filepath.parts[:-1] + (module_name,))
            IMPLICIT_MODULES.add(prefix)
    return Formatter(prettyprinter)


def pretty_dataclass_instance(value: Any, ctx: Any) -> Any:
    cls = type(value)
    kwargs = {}
    for field_def in dataclasses.fields(value):
        # repr is True by default, therefore if this is False, the user
        # has explicitly indicated they don't want to display the field value.
        if not field_def.repr:
            continue

        default = field_def.default
        default_factory: Any = field_def.default_factory
        true_val = getattr(value, field_def.name)
        display_attr = (
            default is default_factory is dataclasses.MISSING
            or (default is not dataclasses.MISSING and default != true_val)
            or (
                default_factory is not dataclasses.MISSING
                and default_factory() != true_val
            )
        )
        if display_attr:
            kwargs[field_def.name] = true_val

    if hasattr(value, "kwargs"):
        kwargs |= value.kwargs

    return prettyprinter.pretty_call(ctx, cls, **kwargs)


def dfield(default: Any, compare: bool = False, repr: bool = False) -> Any:
    # pylint: disable=redefined-builtin
    return dataclasses.field(default=default, compare=compare, repr=repr)


def default_repr(obj: Any) -> str:
    params = ", ".join([f"{k}={v!r}" for k, v in obj.__dict__.items()])
    return f"{obj.__class__.__qualname__}({params})"


def weighted_coin_flip(prob: float) -> bool:
    """Returns True with probability prob."""
    return random.choices([True, False], [prob, 1 - prob])[0]


formatter = init_prettyprinter()
