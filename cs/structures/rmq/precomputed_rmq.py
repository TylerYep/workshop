from .rmq import RMQ


class PrecomputedRMQ(RMQ):
    def __init__(self, elems: list[int]) -> None:
        super().__init__(elems)
        self.rmq_table = [[0] * len(elems) for _ in range(len(elems))]

        for i in range(len(elems)):
            self.rmq_table[i][i] = i

        for i in range(1, len(elems)):
            for j in range(i - 1, -1, -1):
                index1 = self.rmq_table[i - 1][j]
                index2 = self.rmq_table[i][j + 1]
                self.rmq_table[i][j] = self.return_smaller_index(index1, index2)

    def rmq(self, low: int, high: int) -> int:
        if low >= high:
            raise RuntimeError("In the range, low must be lower than high.")

        return self.rmq_table[high - 1][low]
