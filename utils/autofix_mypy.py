from __future__ import annotations

from pathlib import Path

MYPY_OUTPUT = """

"""


def main() -> None:
    lines_changed: dict[str, int] = {}
    for line in MYPY_OUTPUT.split("\n"):
        if not line:
            continue

        filepath, row, _ = extract_details(line)
        all_lines = Path(filepath).read_text(encoding="utf-8")
        lines = all_lines.split("\n")
        try:
            if (
                "found module but no type hints or library stubs" in line
                or "module is installed, but missing library stubs or py.typed marker"
                in line
            ):
                add_import_type_ignore(filepath, lines, row, lines_changed)
            if "Class cannot subclass " in line:
                add_subclass_type_ignore(filepath, lines, row, lines_changed)
            if "unused 'type: ignore' comment" in line:
                remove_unused_type_ignore(filepath, lines, row, lines_changed)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error occurred: {exc}\n when processing{filepath}:{row}")
    print(f"Lines modified: {lines_changed}")


def add_import_type_ignore(
    filepath: str, lines: list[str], row: int, lines_changed: dict[str, int]
) -> None:
    if "# type: ignore" not in lines[row]:
        with open(filepath, "w", encoding="utf-8") as f:
            lines[row] = f"{lines[row]}  # type: ignore[import]"
            f.write("\n".join(lines))
        key = "missing import"
        lines_changed[key] = lines_changed.get(key, 0) + 1


def add_subclass_type_ignore(
    filepath: str, lines: list[str], row: int, lines_changed: dict[str, int]
) -> None:
    if "# type: ignore" not in lines[row]:
        with open(filepath, "w", encoding="utf-8") as f:
            lines[row] = f"{lines[row]}  # type: ignore[misc]"
            f.write("\n".join(lines))
        key = "subclass is type Any"
        lines_changed[key] = lines_changed.get(key, 0) + 1


def remove_unused_type_ignore(
    filepath: str, lines: list[str], row: int, lines_changed: dict[str, int]
) -> None:
    if "  # type: ignore" in lines[row]:
        with open(filepath, "w", encoding="utf-8") as f:
            lines[row] = lines[row][: lines[row].index("  # type: ignore")]
            f.write("\n".join(lines))
        key = "unused type ignore"
        lines_changed[key] = lines_changed.get(key, 0) + 1


def extract_details(flake8_error_line: str) -> tuple[str, int, str]:
    filename, row_str, message_lines = flake8_error_line.split(":")[:3]
    filepath = f"{Path.home()}/robinhood/rh/{filename}"
    row = int(row_str) - 1
    message = "".join(message_lines)
    return filepath, row, message


if __name__ == "__main__":
    main()
