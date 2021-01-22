class RMQ:
    def __init__(self, elems: list[int]) -> None:
        self.elems = elems

    def rmq(self, low: int, high: int) -> int:
        raise NotImplementedError

    def return_smaller_index(self, index1: int, index2: int) -> int:
        if -1 in (index1, index2):
            return index1
        if self.elems[index1] == self.elems[index2]:
            return index1 if index1 < index2 else index2
        return index1 if self.elems[index1] < self.elems[index2] else index2
