import re
import sys
from pathlib import Path


def regex(filepath: str, regexp: str) -> None:
    with Path(filepath).open(encoding="utf-8") as f:
        reg = re.compile(regexp)
        matches = [line[:-1] for line in f if reg.search(line)]
        for m in matches:
            print(m)


def regex_str(line: str, regexp: str) -> None:
    reg = re.compile(regexp)
    print(reg.findall(line))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        regex(args[0], args[1])
    else:
        line_to_search = "1 5 71 13"
        regex_str(line_to_search, args[0])
