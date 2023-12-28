import itertools
from collections import Counter
from pprint import pformat

MAX_WEIGHTS_ON_HANDLE = 6
MAX_WEIGHTS_ON_BAR = 12
HANDLE_WEIGHT = 0.6
CONNECTOR_WEIGHT = 0.8
# WEIGHTS = [4.4] * 4 + [5.5] * 8
WEIGHTS = [2.8] * 4 + [3.3] * 4 + [4.4] * 4 + [10.0] * 2


def calculate_weight_combinations(weights: list[float]) -> None:
    print(f"Weight counts: {dict(Counter(weights))}")
    configs = {}
    for i in range(MAX_WEIGHTS_ON_BAR + 1):
        for config in set(itertools.combinations(weights, i)):
            counts = Counter(config)
            if all(count % 2 == 0 for count in counts.values()):
                result = sum(config) + HANDLE_WEIGHT
                if len(config) > MAX_WEIGHTS_ON_HANDLE:
                    # We already added one handle weight
                    result += HANDLE_WEIGHT + CONNECTOR_WEIGHT
                every_other_elem = config[1::2]
                configs[every_other_elem] = round(result, 2)
    sorted_by_value = sorted(configs.items(), key=lambda e: e[1])
    print(pformat(sorted_by_value))


if __name__ == "__main__":
    calculate_weight_combinations(WEIGHTS)
