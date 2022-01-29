import math
from pprint import pformat

from .rmq import RMQ


class SparseTableRMQ(RMQ):
    def __init__(self, elems: list[int]) -> None:
        super().__init__(elems)
        log_elems = math.floor(math.log2(len(elems))) + 1
        self.rmq_table = [[-1] * len(elems) for _ in range(log_elems)]

        for i in range(len(elems)):
            self.rmq_table[0][i] = i

        for i in range(1, log_elems + 1):
            for j in range(len(elems) - (2**i) + 1):
                index1 = self.rmq_table[i - 1][j]
                index2 = self.rmq_table[i - 1][j + 2 ** (i - 1)]
                self.rmq_table[i][j] = self.return_smaller_index(index1, index2)

    def __repr__(self) -> str:
        # return pformat(np.transpose(np.array(self.rmq_table)))
        return pformat(self.rmq_table)

    def rmq(self, low: int, high: int) -> int:
        if low >= high:
            raise RuntimeError("In the range, low must be lower than high.")

        def get_k(n: int) -> int:
            return 67 - len(bin(-n)) & ~n >> 64

        k = 63 - get_k(high - low)
        index1 = self.rmq_table[k][low]
        index2 = self.rmq_table[k][high - 2**k]
        return self.return_smaller_index(index1, index2)
