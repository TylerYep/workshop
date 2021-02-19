from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(init=False)
class SuffixArray:
    text: str
    suffix_arr: list[int] = field(repr=False)

    def __init__(self, text: str) -> None:
        from cs.algorithms.string.sais import build_suffix_array

        self.text = text + "$"
        self.suffix_arr = build_suffix_array(text)

    def __str__(self) -> str:
        return str([self.text[suffix_index:] for suffix_index in self.suffix_arr])

    def __getitem__(self, key: int) -> int:
        return self.suffix_arr[key]

    def search(self, pattern: str) -> list[int]:
        """
        Returns a list of indices where all matching strings start.
        Uses a two-pass binary search.
        """

        def left_right_binary_search(target: str, is_left: bool) -> int | None:
            """
            Returns the leftmost index of target element,
            or -1 if it cannot be found.
            """
            left, right = 0, len(self.text) - 1
            index = None
            while left <= right:
                mid = left + (right - left) // 2
                mid_val = self.text[self.suffix_arr[mid] :]
                if mid_val.startswith(target):
                    index = mid
                    if is_left:
                        right = mid - 1
                    else:
                        left = mid + 1
                elif mid_val < target:
                    left = mid + 1
                else:
                    right = mid - 1
            return index

        low = left_right_binary_search(pattern, True)
        high = left_right_binary_search(pattern, False)
        if low is None or high is None:
            return []
        return sorted(self.suffix_arr[x] for x in range(low, high + 1))
