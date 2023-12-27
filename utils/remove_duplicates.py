import sys
from pathlib import Path

ROOT_DIR = Path("/Users/tyler.yep/Desktop")


def main(file_name: str) -> None:
    with (ROOT_DIR / file_name).open(encoding="utf-8") as f:
        lines = {line.strip() for line in f.readlines()}
        for line in sorted(lines):
            print(line)


if __name__ == "__main__":
    main(sys.argv[1])
