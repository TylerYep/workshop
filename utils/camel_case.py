import os
import re


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    if name[0] == "_":
        return name[1:]
    return name


def snake_to_camel(name: str) -> str:
    return "".join(word.title() for word in name.split("_"))


def convert_filenames(folder: str) -> None:
    for filename in os.listdir(folder):
        if ".py" in filename or ".w" in filename:
            new_filename = camel_to_snake(filename)
            full_path = os.path.join(folder, filename)
            full_new_path = os.path.join(folder, new_filename)
            os.rename(full_path, full_new_path)
