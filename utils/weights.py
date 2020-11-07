import itertools
from pprint import pprint
from typing import List

MAX_WEIGHTS_ON_HANDLE = 6
HANDLE_WEIGHT = 0.6
CONNECTOR_WEIGHT = 0.8
# WEIGHTS = [4.4] * 4 + [5.5] * 8
WEIGHTS = [2.8] * 4 + [3.3] * 4 + [4.4] * 4


def calculate_weight_combinations(weights: List[float]) -> None:
    configs = {}
    for i in range(len(weights) + 1):
        for config in set(itertools.combinations(weights, i)):
            counts = {}
            for w in config:
                if w not in counts:
                    counts[w] = 0
                counts[w] += 1

            for count in counts.values():
                if count % 2 != 0:
                    break
            else:
                result = sum(config) + HANDLE_WEIGHT
                if len(config) > MAX_WEIGHTS_ON_HANDLE:
                    # We already added one handle weight
                    result += HANDLE_WEIGHT + CONNECTOR_WEIGHT
                every_other_elem = config[1::2]
                configs[every_other_elem] = round(result, 2)
    sorted_by_value = sorted(configs.items(), key=lambda e: e[1])
    pprint(sorted_by_value)


if __name__ == "__main__":
    calculate_weight_combinations(WEIGHTS)
