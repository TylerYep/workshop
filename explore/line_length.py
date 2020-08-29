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
    for root, _, files in os.walk(project):
        for filename in files:
            if filename.endswith(".py"):
                full_src_path = os.path.join(root, filename)
                with open(full_src_path) as f:
                    for line in f:
                        length = len(line) - 1
                        if length > 0:
                            counts[length] += 1
    pprint(dict(counts))

    plt.bar(list(counts.keys()), counts.values(), color="g")
    plt.show()


def main() -> None:
    args = init_pipeline()
    count_project_lines(args.project)


if __name__ == "__main__":
    main()
