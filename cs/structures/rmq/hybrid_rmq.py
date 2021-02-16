import math

from .rmq import RMQ
from .sparse_table_rmq import SparseTableRMQ


class HybridRMQ(RMQ):
    def __init__(self, elems: list[int]) -> None:
        super().__init__(elems)
        self.block_size = max(1, math.floor(math.log2(len(elems))))
        self.block_mins = []
        block_min_vals = []
        for i in range(0, len(elems), self.block_size):
            curr_min = i
            for j in range(i + 1, min(i + self.block_size, len(elems))):
                curr_min = self.return_smaller_index(j, curr_min)
            self.block_mins.append(curr_min)
            block_min_vals.append(elems[curr_min])

        self.summary_rmq = SparseTableRMQ(block_min_vals)

    def rmq(self, low: int, high: int) -> int:
        if low >= high:
            raise RuntimeError("In the range, low must be lower than high.")

        min_index = -1
        if high - low < self.block_size:
            for i in range(low, high):
                min_index = self.return_smaller_index(i, min_index)
            return min_index

        start_block = math.ceil(low / self.block_size)
        end_block = math.floor(high / self.block_size)

        if start_block < end_block:
            block_min_index = self.summary_rmq.rmq(start_block, end_block)
            min_index = self.block_mins[block_min_index]

        for i in range(low, min(high, start_block * self.block_size)):
            min_index = self.return_smaller_index(i, min_index)

        for i in range(max(low, end_block * self.block_size), high):
            min_index = self.return_smaller_index(i, min_index)
        return min_index
