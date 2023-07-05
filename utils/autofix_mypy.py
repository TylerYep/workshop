from __future__ import annotations

from pathlib import Path

MYPY_OUTPUT = """

"""
ADD_ALL_TYPE_IGNORES = True


def main() -> None:
    """
    Run type-checking and copy+paste all errors into the output above.
    Then run this function.

    To add error codes, find and replace:
    # type: ignore.*\n
    \n
    """
    lines_changed: dict[str, int] = {}
    for line in MYPY_OUTPUT.split("\n"):
        if not line:
            continue

        filepath, row, is_note, error_code = extract_details(line)
        if is_note:
            continue

        all_lines = Path(filepath).read_text(encoding="utf-8")
        lines = all_lines.split("\n")
        try:
            if (
                "unused 'type: ignore' comment" in line
                or 'unused "type: ignore" comment' in line
            ):
                remove_unused_type_ignore(filepath, lines, row, lines_changed)
            elif ADD_ALL_TYPE_IGNORES:
                add_type_ignore(
                    filepath,
                    lines,
                    row,
                    lines_changed,
                    error_code,
                    context="added_type_ignore",
                )
            elif (
                "found module but no type hints or library stubs" in line
                or "module is installed, but missing library stubs or py.typed marker"
                in line
            ):
                assert error_code == "import"
                add_type_ignore(
                    filepath,
                    lines,
                    row,
                    lines_changed,
                    error_code,
                    context="missing_import",
                )
            elif "Class cannot subclass " in line:
                assert error_code == "misc"
                add_type_ignore(
                    filepath,
                    lines,
                    row,
                    lines_changed,
                    error_code,
                    context="subclass_has_type_Any",
                )
            else:
                print(f"Line not handled: {line}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error occurred: {exc}\n when processing{filepath}:{row}")
    print(f"Lines modified: {lines_changed}")


def add_type_ignore(  # pylint: disable=too-many-arguments
    filepath: Path,
    lines: list[str],
    row: int,
    lines_changed: dict[str, int],
    error_code: str,
    context: str,
) -> None:
    if "# type: ignore" not in lines[row]:
        with filepath.open("w", encoding="utf-8") as f:
            lines[row] = f"{lines[row]}  # type: ignore[{error_code}]"
            f.write("\n".join(lines))
        lines_changed[context] = lines_changed.get(context, 0) + 1


def remove_unused_type_ignore(
    filepath: Path, lines: list[str], row: int, lines_changed: dict[str, int]
) -> None:
    ignore = "  # type: ignore"
    if ignore in lines[row]:
        with filepath.open("w", encoding="utf-8") as f:
            lines[row] = lines[row][: lines[row].index(ignore)]
            f.write("\n".join(lines))
        key = "unused type ignore"
        lines_changed[key] = lines_changed.get(key, 0) + 1


def extract_details(mypy_error_line: str) -> tuple[Path, int, bool, str]:
    # After the 3rd index is the type error message (could have more colons).
    filename, row_str, error_or_note = mypy_error_line.split(":")[:3]
    filepath = Path.home() / f"robinhood/rh/{filename}"
    row = int(row_str) - 1
    is_note = error_or_note.strip() == "note"
    if is_note or "[" not in mypy_error_line:
        error_code = ""
    else:
        error_code = mypy_error_line[mypy_error_line.rindex("[") + 1 : -1]
    return filepath, row, is_note, error_code


if __name__ == "__main__":
    main()
