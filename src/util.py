import prettyprinter
from prettyprinter.prettyprinter import IMPLICIT_MODULES

prettyprinter.install_extras(include=frozenset({"python", "dataclasses"}))
IMPLICIT_MODULES.add("src.structures.graph")

formatter = prettyprinter
