from __future__ import annotations

from pathlib import Path

FLAKE8_OUTPUT = """

"""


def main() -> None:
    lines_changed: dict[str, int] = {}
    for line in FLAKE8_OUTPUT.split("\n"):
        if not line:
            continue

        filepath, row, col, _ = extract_details(line)
        all_lines = Path(filepath).read_text(encoding="utf-8")
        lines = all_lines.split("\n")
        try:
            if "from __future__ import annotations" in line:
                add_future_annotations(filepath, all_lines, lines, lines_changed)
            elif "E231 missing whitespace after" in line:
                fix_trailing_commas(filepath, lines, row, col, lines_changed)
            elif "F541 f-string is missing placeholders" in line:
                fix_empty_f_strings(filepath, lines, row, col, lines_changed)
            elif "E265 block comment should start with '# '" in line:
                fix_missing_comment_space(filepath, lines, row, col, lines_changed)
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Error occurred: {exc}\n{filepath}\n{line}\n")
    print(f"Lines modified: {lines_changed}")


def add_future_annotations(
    filepath: Path, all_lines: str, lines: list[str], lines_changed: dict[str, int]
) -> None:
    add_line = "from __future__ import annotations"
    if lines[0] != add_line:
        with filepath.open("w", encoding="utf-8") as f:
            f.write(f"{add_line}\n{all_lines}")
        key = "future_annotations"
        lines_changed[key] = lines_changed.get(key, 0) + 1


def fix_trailing_commas(
    filepath: Path, lines: list[str], row: int, col: int, lines_changed: dict[str, int]
) -> None:
    if lines[row][col] == ",":
        with filepath.open("w", encoding="utf-8") as f:
            lines[row] = lines[row][:col] + lines[row][col + 1 :]
            f.write("\n".join(lines))
            key = "trailing comma"
            lines_changed[key] = lines_changed.get(key, 0) + 1


def fix_empty_f_strings(
    filepath: Path, lines: list[str], row: int, col: int, lines_changed: dict[str, int]
) -> None:
    if lines[row][col] == "f":
        with filepath.open("w", encoding="utf-8") as f:
            lines[row] = lines[row][:col] + lines[row][col + 1 :]
            f.write("\n".join(lines))
            key = "unnecessary f-string"
            lines_changed[key] = lines_changed.get(key, 0) + 1


def fix_missing_comment_space(
    filepath: Path, lines: list[str], row: int, col: int, lines_changed: dict[str, int]
) -> None:
    if lines[row][col] == "#":
        with filepath.open("w", encoding="utf-8") as f:
            lines[row] = lines[row].replace("#", "# ")
            f.write("\n".join(lines))
            key = "missing comment space"
            lines_changed[key] = lines_changed.get(key, 0) + 1


def extract_details(flake8_error_line: str) -> tuple[Path, int, int, str]:
    filename, row_str, col_str, message_lines = flake8_error_line.split(":")[:4]
    filepath = Path.home() / f"robinhood/rh/{filename}"
    row = int(row_str) - 1
    col = int(col_str) - 1
    message = "".join(message_lines)
    return filepath, row, col, message


if __name__ == "__main__":
    main()
