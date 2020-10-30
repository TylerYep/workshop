import os
import random

import prettyprinter
from prettyprinter.prettyprinter import IMPLICIT_MODULES

prettyprinter.install_extras(include={"python", "dataclasses"})
for root, _, files in os.walk("src/structures"):
    for filename in files:
        if filename.endswith(".py") and "__" not in filename:
            module_name = os.path.splitext(filename)[0]
            parts = root.split(os.sep) + [module_name]
            IMPLICIT_MODULES.add(".".join(parts))

formatter = prettyprinter


def weighted_coin_flip(prob: float) -> bool:
    """ Returns True with probability prob. """
    return random.choices([True, False], [prob, 1 - prob])[0]
