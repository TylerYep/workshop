import argparse
import os
from collections import defaultdict
from pprint import pprint
from typing import Dict

import matplotlib.pyplot as plt


def init_pipeline() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Line Length Histogram")
    # fmt: off
    parser.add_argument("project", type=str,
                        help="version of the code to read")
    return parser.parse_args()
    # fmt: on


def count_project_lines(project: str) -> None:
    counts: Dict[int, int] = defaultdict(int)
    lines_above_88 = 0
    for root, _, files in os.walk(project):
        for filename in files:
            if filename.endswith(".py"):
                full_src_path = os.path.join(root, filename)
                try:
                    with open(full_src_path) as f:
                        for line in f:
                            length = len(line) - 1
                            if length > 0:
                                counts[length] += 1
                            if length > 88:
                                lines_above_88 += 1
                                print(line)
                except UnicodeDecodeError:
                    print(full_src_path)

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
