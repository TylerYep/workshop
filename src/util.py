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
    prettyprinter.install_extras(include={"python", "dataclasses"})
    for root, _, files in os.walk("src"):
        for filename in files:
            if filename.endswith(".py") and "__" not in filename:
                module_name = os.path.splitext(filename)[0]
                prefix = ".".join(root.split(os.sep) + [module_name])
                IMPLICIT_MODULES.add(prefix)
    return prettyprinter


def weighted_coin_flip(prob: float) -> bool:
    """ Returns True with probability prob. """
    return random.choices([True, False], [prob, 1 - prob])[0]


formatter = init_prettyprinter()
