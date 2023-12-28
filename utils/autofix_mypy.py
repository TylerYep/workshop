# pylint: disable=too-many-branches
from __future__ import annotations

import traceback
import warnings
from pathlib import Path

MYPY_OUTPUT = """

"""
ADD_ALL_TYPE_IGNORES = True

# Replace cache path with path to your local rh directory.
ROOT_DIR = Path.home() / "robinhood/rh2"
MYPY_OUTPUT = MYPY_OUTPUT.replace(
    MYPY_OUTPUT[1 : MYPY_OUTPUT.index("/rh") + len("/rh")], str(ROOT_DIR)
).replace("error:\n", "error: ")


def main() -> None:
    """
    Run type-checking and copy+paste all errors into the output above.
    Then run this function.

    To add error codes, find and replace:
    # type: ignore.*\n
    \n
    """
    lines_changed: dict[str, int] = {}
    insert_extra_lines: dict[int, str] = {}
    for mypy_error_line in MYPY_OUTPUT.split("\n"):
        if not mypy_error_line:
            continue

        if "rh" not in mypy_error_line or "error: " not in mypy_error_line:
            continue

        filepath, row, is_note, error_code = extract_details(mypy_error_line)
        if is_note:
            continue

        all_lines = filepath.read_text(encoding="utf-8")
        lines = all_lines.split("\n")
        try:
            if "nused 'type: ignore' comment" in mypy_error_line.replace('"', "'"):
                remove_unused_type_ignore(filepath, lines, row, lines_changed)
            elif (
                "found module but no type hints or library stubs" in mypy_error_line
                or "module is installed, but missing library stubs or py.typed marker"
                in mypy_error_line
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
            elif "Class cannot subclass " in mypy_error_line:
                assert error_code == "misc"
                add_type_ignore(
                    filepath,
                    lines,
                    row,
                    lines_changed,
                    error_code,
                    context="subclass_has_type_Any",
                )
            elif "Missing type parameters for generic type " in mypy_error_line:
                add_type_ignore(
                    filepath,
                    lines,
                    row,
                    lines_changed,
                    error_code,
                    context="generic_type",
                )
            elif "is not subscriptable, use 'typing." in mypy_error_line.replace(
                '"', "'"
            ):
                add_future_annotations(
                    filepath, lines, lines_changed, context="needs_future_annotations"
                )
            elif "type: ignore' comment without error code" in mypy_error_line.replace(
                '"', "'"
            ):
                add_error_code(
                    filepath,
                    mypy_error_line,
                    lines,
                    row,
                    lines_changed,
                    context="add_error_code",
                )
            elif "is not using @override but is overriding a method" in mypy_error_line:
                add_override(
                    lines,
                    row,
                    lines_changed,
                    insert_extra_lines,
                    context="override",
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
                print(f"Line not handled: {mypy_error_line}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error occurred: {exc}\n when processing{filepath}:{row}")
            traceback.print_exc()

    write_extra_lines(filepath, lines, insert_extra_lines)
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
        new_line = add_to_existing_type_ignores(lines[row], error_code)
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


def add_override(
    lines: list[str],
    row: int,
    lines_changed: dict[str, int],
    insert_extra_lines: dict[int, str],
    context: str,
) -> None:
    indent = len(lines[row]) - len(lines[row].lstrip())
    insert_extra_lines[row] = f"{' ' * indent}@override\n"
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


def add_error_code(  # pylint: disable=too-many-arguments
    filepath: Path,
    mypy_error_line: str,
    lines: list[str],
    row: int,
    lines_changed: dict[str, int],
    context: str,
) -> None:
    start_tag = 'consider "type: ignore['
    end_tag = ']" instead)'
    new_error_code = mypy_error_line[
        mypy_error_line.rindex(start_tag)
        + len(start_tag) : mypy_error_line.index(end_tag)
    ]
    with filepath.open("w", encoding="utf-8") as f:
        lines[row] = add_to_existing_type_ignores(lines[row], new_error_code)
        f.write("\n".join(lines))
    lines_changed[context] = lines_changed.get(context, 0) + 1


def extract_details(mypy_error_line: str) -> tuple[Path, int, bool, str]:
    # After the 3rd index is the type error message (could have more colons).
    filename, row_str, error_or_note = mypy_error_line.split(":")[:3]
    filepath = ROOT_DIR / filename
    row = int(row_str) - 1
    is_note = error_or_note.strip() == "note"
    if is_note:
        error_code = ""
    elif "[" not in mypy_error_line:
        warnings.warn(
            f"Error code not found in {mypy_error_line}. "
            "Did you turn on `show_error_codes=True in your mypy config file?",
            stacklevel=2,
        )
    else:
        error_code = mypy_error_line[mypy_error_line.rindex("[") + 1 : -1]
    return filepath, row, is_note, error_code


def add_to_existing_type_ignores(line: str, error_code: str) -> str:
    ignore_key = "# type: ignore"
    if "# type:ignore" in line:
        line = line.replace("# type:ignore", ignore_key)
    type_ignore_start = line.rindex(ignore_key)
    start_bracket = type_ignore_start + len(ignore_key)
    parts = line[start_bracket:]
    if parts and parts[0] == "[":
        type_ignore_end = parts.index("]")
        error_codes = {code.strip() for code in parts[1:type_ignore_end].split(",")}
        error_codes.add(error_code)
        return (
            line[: start_bracket + 1]
            + ",".join(sorted(error_codes))
            + line[start_bracket + type_ignore_end :]
        )
    return line[:start_bracket] + f"[{error_code}]" + line[start_bracket:]


def write_extra_lines(
    filepath: Path, lines: list[str], insert_extra_lines: dict[int, str]
) -> None:
    for line_num_to_insert_before, new_line in sorted(
        insert_extra_lines.items(), key=lambda x: x[0], reverse=True
    ):
        lines.insert(line_num_to_insert_before, new_line)

    with filepath.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
