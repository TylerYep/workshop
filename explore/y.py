# type: ignore
# pylint: disable-all
import queue
import random
import unittest

import binomialheap


class BinomialHeap:
    def __init__(self):
        self.head = BinomialHeap.Node()  # Dummy node

    def empty(self):
        return self.head.next is None

    def __len__(self):
        result = 0
        node = self.head.next
        while node is not None:
            result |= 1 << node.rank
            node = node.next
        return result

    def clear(self):
        self.head.next = None

    def enqueue(self, val):
        self._merge(BinomialHeap.Node(val))

    def peek(self):
        if self.head.next is None:
            raise Exception("Empty heap")
        result = None
        node = self.head.next
        while node is not None:
            if result is None or node.value < result:
                result = node.value
            node = node.next
        return result

    def dequeue(self):
        if self.head.next is None:
            raise Exception("Empty heap")
        min_ = None
        nodebeforemin = None
        prevnode = self.head
        while True:
            node = prevnode.next
            if node is None:
                break
            if min_ is None or node.value < min_:
                min_ = node.value
                nodebeforemin = prevnode
            prevnode = node
        assert min_ is not None and nodebeforemin is not None
        minnode = nodebeforemin.next
        nodebeforemin.next = minnode.next
        minnode.next = None
        self._merge(minnode.remove_root())
        return min_

    # Moves all the values in the given heap into this heap
    def merge(self, other):
        if other is self:
            raise ValueError()
        self._merge(other.head.next)
        other.head.next = None

    def _merge(self, other):
        assert self.head.rank == -1
        assert other is None or other.rank >= 0
        this = self.head.next
        self.head.next = None
        prevtail = None
        tail = self.head
        while this is not None or other is not None:
            if other is None or (this is not None and this.rank <= other.rank):
                node = this
                this = this.next
            else:
                node = other
                other = other.next
            node.next = None
            assert tail.next is None
            if tail.rank < node.rank:
                prevtail = tail
                tail.next = node
                tail = node
            elif tail.rank == node.rank + 1:
                assert prevtail is not None
                node.next = tail
                prevtail.next = node
                prevtail = node
            elif tail.rank == node.rank:
                # Merge nodes
                if tail.value <= node.value:
                    node.next = tail.down
                    tail.down = node
                    tail.rank += 1
                else:
                    assert prevtail is not None
                    tail.next = node.down
                    node.down = tail
                    node.rank += 1
                    tail = node
                    prevtail.next = node
            else:
                raise AssertionError()

    # For unit tests
    def check_structure(self):
        head = self.head
        if head.value is not None or head.rank != -1:
            raise AssertionError("Head must be dummy node")
        # Check chain of nodes and their children
        head.check_structure(True, None)

    # ---- Helper class: Binomial heap node ----
    class Node:
        def __init__(self, val=None):
            self.value = val
            if val is None:  # Dummy sentinel node at head of list
                self.rank = -1
            else:  # Regular node
                self.rank = 0
            self.down = None
            self.next = None

        def remove_root(self):
            assert self.next is None
            result = None
            node = self.down
            while (
                node is not None
            ):  # Reverse the order of nodes from descending rank to ascending rank
                next_ = node.next
                node.next = result
                result = node
                node = next_
            return result

        # For unit tests
        def check_structure(self, ismain, lowerbound):
            # Basic checks
            if (self.rank < 0) != (self.value is None):
                raise AssertionError("Invalid node rank or value")
            if ismain != (lowerbound is None):
                raise AssertionError("Invalid arguments")
            if not ismain and self.value < lowerbound:
                raise AssertionError("Min-heap property violated")
            # Check children and non-main chains
            if self.rank > 0:
                if self.down is None or self.down.rank != self.rank - 1:
                    raise AssertionError("Down node absent or has invalid rank")
                self.down.check_structure(False, self.value)
                if not ismain:
                    if self.next is None or self.next.rank != self.rank - 1:
                        raise AssertionError("Next node absent or has invalid rank")
                    self.next.check_structure(False, lowerbound)
            elif self.down is not None:
                raise AssertionError("Down node must be absent")
            # Check main chain
            if ismain and self.next is not None:
                if self.next.rank <= self.rank:
                    raise AssertionError("Next node has invalid rank")
                self.next.check_structure(True, None)


class BinomialHeapTest(unittest.TestCase):
    def test_size_1(self):
        h = binomialheap.BinomialHeap()
        h.enqueue(3)
        h.check_structure()
        self.assertEqual(1, len(h))
        self.assertEqual(3, h.peek())
        self.assertEqual(3, h.dequeue())
        h.check_structure()
        self.assertEqual(0, len(h))

    def test_size_2(self):
        h = binomialheap.BinomialHeap()
        h.enqueue(4)
        h.enqueue(2)
        h.check_structure()
        self.assertEqual(2, len(h))
        self.assertEqual(2, h.peek())
        self.assertEqual(2, h.dequeue())
        h.check_structure()
        self.assertEqual(1, len(h))
        self.assertEqual(4, h.peek())
        self.assertEqual(4, h.dequeue())
        h.check_structure()
        self.assertEqual(0, len(h))

    def test_size_7(self):
        h = binomialheap.BinomialHeap()
        h.enqueue(2)
        h.enqueue(7)
        h.enqueue(1)
        h.enqueue(8)
        h.enqueue(3)
        h.check_structure()
        h.enqueue(1)
        h.enqueue(4)
        h.check_structure()
        self.assertEqual(7, len(h))
        self.assertEqual(1, h.dequeue())
        self.assertEqual(6, len(h))
        self.assertEqual(1, h.dequeue())
        self.assertEqual(5, len(h))
        self.assertEqual(2, h.dequeue())
        self.assertEqual(4, len(h))
        self.assertEqual(3, h.dequeue())
        self.assertEqual(3, len(h))
        h.check_structure()
        self.assertEqual(4, h.dequeue())
        self.assertEqual(2, len(h))
        self.assertEqual(7, h.dequeue())
        self.assertEqual(1, len(h))
        self.assertEqual(8, h.dequeue())
        self.assertEqual(0, len(h))
        h.check_structure()

    def test_against_list_randomly(self):
        TRIALS = 1000
        MAX_SIZE = 300
        RANGE = 1000

        heap = binomialheap.BinomialHeap()
        for _ in range(TRIALS):
            size = random.randrange(MAX_SIZE)
            values = [random.randrange(RANGE) for _ in range(size)]
            for val in values:
                heap.enqueue(val)

            values.sort()
            for val in values:
                self.assertEqual(val, heap.dequeue())

            self.assertTrue(heap.empty())
            heap.clear()

    def test_against_python_priority_queue_randomly(self):
        TRIALS = 10000
        ITER_OPS = 100
        RANGE = 10000

        que = queue.PriorityQueue()
        heap = binomialheap.BinomialHeap()
        size = 0
        for i in range(TRIALS):
            if i % 300 == 0:
                print(f"Progress: {i / TRIALS:.0%}")
            op = random.randrange(100)

            if op < 1:  # Clear
                heap.check_structure()
                for _ in range(size):
                    self.assertEqual(heap.dequeue(), que.get(False))
                size = 0

            elif op < 2:  # Peek
                heap.check_structure()
                if size > 0:
                    val = que.get(False)
                    self.assertEqual(heap.peek(), val)
                    que.put(val)

            elif op < 70:  # Enqueue/merge
                merge = not op < 60
                sink = binomialheap.BinomialHeap() if merge else heap
                n = random.randint(1, ITER_OPS)
                for _ in range(n):
                    val = random.randrange(RANGE)
                    que.put(val)
                    sink.enqueue(val)
                if merge:
                    heap.merge(sink)
                    self.assertEqual(len(sink), 0)
                size += n

            elif op < 100:  # Dequeue
                n = min(random.randint(1, ITER_OPS), size)
                for _ in range(n):
                    self.assertEqual(heap.dequeue(), que.get(False))
                size -= n

            else:
                raise AssertionError()

            self.assertEqual(que.qsize(), size)
            self.assertEqual(len(heap), size)
            self.assertEqual(que.empty(), size == 0)
            self.assertEqual(heap.empty(), size == 0)


if __name__ == "__main__":
    unittest.main()
