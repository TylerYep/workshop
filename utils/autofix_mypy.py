from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path.home() / "robinhood/rh2"
MYPY_OUTPUT = """

"""
ADD_ALL_TYPE_IGNORES = False


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
            if "nused 'type: ignore' comment" in line.replace('"', "'"):
                remove_unused_type_ignore(filepath, lines, row, lines_changed)
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
            elif "Missing type parameters for generic type " in line:
                add_type_ignore(
                    filepath,
                    lines,
                    row,
                    lines_changed,
                    error_code,
                    context="generic_type",
                )
            elif "is not subscriptable, use 'typing." in line.replace('"', "'"):
                add_future_annotations(
                    filepath, lines, lines_changed, context="needs_future_annotations"
                )
            elif ADD_ALL_TYPE_IGNORES:
                add_type_ignore(
                    filepath,
                    lines,
                    row,
                    lines_changed,
                    error_code,
                    context="added_type_ignore",
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
    if "# type: ignore" in lines[row]:
        line_without_type_ignore, error_codes = extract_type_ignores(lines[row])
        error_codes.add(error_code)
        error_codes_str = ",".join(sorted(error_codes))
        new_line = f"{line_without_type_ignore}  # type: ignore[{error_codes_str}]"
    else:
        new_line = f"{lines[row]}  # type: ignore[{error_code}]"

    with filepath.open("w", encoding="utf-8") as f:
        lines[row] = new_line
        f.write("\n".join(lines))
    lines_changed[context] = lines_changed.get(context, 0) + 1


def add_future_annotations(
    filepath: Path, lines: list[str], lines_changed: dict[str, int], context: str
) -> None:
    with filepath.open("w", encoding="utf-8") as f:
        lines.insert(0, "from __future__ import annotations")
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
    filepath = ROOT_DIR / filename
    row = int(row_str) - 1
    is_note = error_or_note.strip() == "note"
    if is_note or "[" not in mypy_error_line:
        error_code = ""
    else:
        error_code = mypy_error_line[mypy_error_line.rindex("[") + 1 : -1]
    return filepath, row, is_note, error_code


def extract_type_ignores(line: str) -> tuple[str, set[str]]:
    assert "# type: ignore" in line
    type_ignore_start = line.rindex("# type: ignore")
    parts = line[type_ignore_start + len("# type: ignore") :]
    print(parts)
    if parts[0] == "[":
        type_ignore_end = parts.index("]")
        error_codes = {
            error_code.strip() for error_code in parts[1:type_ignore_end].split(",")
        }
        new_line = (
            line[:type_ignore_start]
            + line[type_ignore_start + len("# type: ignore") + type_ignore_end + 1 :]
        )
        return new_line, error_codes
    return line.replace("# type: ignore", ""), []


if __name__ == "__main__":
    main()
