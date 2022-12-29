from __future__ import annotations

from pathlib import Path

FLAKE8_OUTPUT = """

"""


def main() -> None:
    lines_changed: dict[str, int] = {}
    for line in FLAKE8_OUTPUT.split("\n"):
        if line:
            filepath, row, col, _ = extract_details(line)
            all_lines = Path(filepath).read_text(encoding="utf-8")
            lines = all_lines.split("\n")

            if "from __future__ import annotations" in line:
                add_future_annotations(filepath, all_lines, lines, lines_changed)
            elif "E231 missing whitespace after" in line:
                fix_trailing_commas(filepath, lines, row, col, lines_changed)
            elif "F541 f-string is missing placeholders" in line:
                fix_empty_f_strings(filepath, lines, row, col, lines_changed)
    print(f"Lines modified: {lines_changed}")


def add_future_annotations(
    filepath: str, all_lines: str, lines: list[str], lines_changed: dict[str, int]
) -> None:
    add_line = "from __future__ import annotations"
    if lines[0] != add_line:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{add_line}\n{all_lines}")
        key = "future_annotations"
        lines_changed[key] = lines_changed.get(key, 0) + 1


def fix_trailing_commas(
    filepath: str, lines: list[str], row: int, col: int, lines_changed: dict[str, int]
) -> None:
    if lines[row][col] == ",":
        with open(filepath, "w", encoding="utf-8") as f:
            lines[row] = lines[row][:col] + lines[row][col + 1 :]
            f.write("\n".join(lines))
            key = "trailing comma"
            lines_changed[key] = lines_changed.get(key, 0) + 1


def fix_empty_f_strings(
    filepath: str, lines: list[str], row: int, col: int, lines_changed: dict[str, int]
) -> None:
    if lines[row][col] == "f":
        with open(filepath, "w", encoding="utf-8") as f:
            lines[row] = lines[row][:col] + lines[row][col + 1 :]
            f.write("\n".join(lines))
            key = "unnecessary f-string"
            lines_changed[key] = lines_changed.get(key, 0) + 1


def extract_details(flake8_error_line: str) -> tuple[str, int, int, str]:
    filename, row_str, col_str, message_lines = flake8_error_line.split(":")[:4]
    filepath = f"{Path.home()}/robinhood/rh/{filename}"
    row = int(row_str) - 1
    col = int(col_str) - 1
    message = "".join(message_lines)
    return filepath, row, col, message


if __name__ == "__main__":
    main()
