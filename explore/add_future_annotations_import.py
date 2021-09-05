def main() -> None:
    FILE_NAMES = []
    for filename in FILE_NAMES:
        filename = filename.split(":")[0]
        with open(filename, "w", encoding="utf-8") as f:
            lines = f.read()
            f.write("from __future__ import annotations\n" + lines)
