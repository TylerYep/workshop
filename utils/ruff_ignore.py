from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path.home() / "robinhood/rh"
RUFF_OUTPUT = """

"""


def main() -> None:
    error_messages: dict[str, str] = {}
    for line in RUFF_OUTPUT.split("\n"):
        if not line:
            continue

        if line.startswith("warning"):
            continue

        _, _, _, error = extract_details(line)
        error_code, error_message = error[1:].split(" ", maxsplit=1)
        if error_code not in error_messages:
            error_messages[error_code] = error_message
    for error_code, error_message in sorted(error_messages.items()):
        spaces = 8 - len(error_code)
        print(f'"{error_code}",{" " * spaces}# {error_message}')


def extract_details(ruff_error_line: str) -> tuple[Path, int, int, str]:
    filename, row_str, col_str, message_lines = ruff_error_line.split(":")[:4]
    filepath = ROOT_DIR / filename
    row = int(row_str) - 1
    col = int(col_str) - 1
    message = "".join(message_lines)
    return filepath, row, col, message


if __name__ == "__main__":
    main()
