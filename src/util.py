import os

import prettyprinter
from prettyprinter.prettyprinter import IMPLICIT_MODULES

prettyprinter.install_extras(include={"python", "dataclasses"})
for filename in os.listdir("src/structures"):
    module_name = os.path.splitext(filename)[0]
    if "__" not in module_name:
        IMPLICIT_MODULES.add(f"src.structures.{module_name}")

formatter = prettyprinter
