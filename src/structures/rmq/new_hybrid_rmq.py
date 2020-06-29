import math
from typing import List

from .rmq import RMQ
from .sparse_table_rmq import SparseTableRMQ


class NewHybridRMQ(RMQ):
    def __init__(self, elems: List[int]) -> None:
        super().__init__(elems)
        sparse_table = SparseTableRMQ(elems)
        self.block_size = math.floor(math.log2(len(elems)))
        if self.block_size == 0:
            self.block_size = 1
        self.blocks = [
            sparse_table.rmq(low, min(low + self.block_size, len(elems)))
            for low in range(0, len(elems) - self.block_size, self.block_size)
        ]

    def rmq(self, low: int, high: int) -> int:
        start_block = math.ceil(low / self.block_size)
        end_block = math.floor(high / self.block_size)

        min_index = -1
        for i in range(start_block, end_block):
            min_index = self.return_smaller_index(self.blocks[i], min_index)

        for i in range(low, min(high, start_block * self.block_size)):
            min_index = self.return_smaller_index(i, min_index)

        for i in range(max(low, end_block * self.block_size), high):
            min_index = self.return_smaller_index(i, min_index)
        return min_index
