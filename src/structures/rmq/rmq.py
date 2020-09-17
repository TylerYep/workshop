from typing import List, Optional


class RMQ:
    def __init__(self, elems: List[int]) -> None:
        self.elems = elems

    def rmq(self, low: int, high: int) -> int:
        raise NotImplementedError

    def return_smaller_index(self, index1: Optional[int], index2: Optional[int]) -> int:
        # Can return index2 but shouldn't happen realistically
        assert index1 is not None
        if index2 is None:
            return index1
        if self.elems[index1] == self.elems[index2]:
            return index1 if index1 < index2 else index2
        return index1 if self.elems[index1] < self.elems[index2] else index2
