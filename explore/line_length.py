import argparse
from collections import defaultdict
from pathlib import Path
from pprint import pprint

import matplotlib.pyplot as plt


def init_pipeline() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Line Length Histogram")
    parser.add_argument("project", type=str, help="version of the code to read")
    return parser.parse_args()


def count_project_lines(project: str) -> None:
    counts: dict[int, int] = defaultdict(int)
    lines_above_88 = 0
    for filepath in Path(project).rglob("*.py"):
        try:
            with open(filepath) as f:
                for line in f:
                    length = len(line) - 1
                    if length > 0:
                        counts[length] += 1
                    if length > 88:
                        lines_above_88 += 1
                        print(line)
        except UnicodeDecodeError:
            print(filepath)

    pprint(dict(counts))
    print(lines_above_88)

    lengths = min(len(counts), 130)
    plt.bar(range(lengths), [counts[i] for i in range(lengths)], color="g")

    total_lines = sum(counts.values())
    cumulative = 0
    marker = 0
    for i in range(lengths):
        if cumulative > total_lines * 0.98:
            break
        cumulative += counts[i]
        marker += 1

    # plt.axvline(x=marker, color="b", linestyle="-")
    plt.show()


def main() -> None:
    args = init_pipeline()
    count_project_lines(args.project)


if __name__ == "__main__":
    main()
