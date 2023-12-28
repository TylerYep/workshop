import re
from pathlib import Path


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    if name[0] == "_":
        return name[1:]
    return name


def snake_to_camel(name: str) -> str:
    return "".join(word.title() for word in name.split("_"))


def convert_filenames(folder: str) -> None:
    folder_path = Path(folder)
    for filepath in folder_path.glob("*.py"):
        result = camel_to_snake(str(filepath))
        full_new_path = filepath.with_name(result)
        filepath.rename(full_new_path)
