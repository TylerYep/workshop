from typing import List, Optional

from ..algorithms.sais import sais, to_rank_array


class SuffixArray:
    def __init__(self, text: str) -> None:
        self.text = text + "$"
        self.suffix_arr: List[int] = sais(to_rank_array(text))

    def __getitem__(self, key: int) -> int:
        return self.suffix_arr[key]

    def __repr__(self) -> str:
        return str([self.text[suffix_index:] for suffix_index in self.suffix_arr])

    def search(self, pattern: str) -> List[int]:
        """ Returns a list of indices where all matching strings start.
        Uses a two-pass binary search.
        """

        def left_right_binary_search(target: str, is_left: bool) -> Optional[int]:
            """ Returns the leftmost index of target element, or -1 if it cannot be found. """
            left = 0
            right = len(self.text) - 1
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
                elif mid_val > target:
                    right = mid - 1
            return index

        low = left_right_binary_search(pattern, True)
        high = left_right_binary_search(pattern, False)
        if low is None or high is None:
            return []
        return sorted([self.suffix_arr[x] for x in range(low, high + 1)])


if __name__ == "__main__":
    s = SuffixArray("nonsense")
    result = s.search("nse")
    assert result == [2, 5], result
    result = s.search("nonsense")
    assert result == [0], result
    result = s.search("no")
    assert result == [0], result
    result = s.search("n")
    assert result == [0, 2, 5], result
    result = s.search("")
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8], result

    s = SuffixArray("h")
    result = s.search("h")
    assert result == [0], result

    s = SuffixArray("HAHAHAHAHA")
    print(s)
