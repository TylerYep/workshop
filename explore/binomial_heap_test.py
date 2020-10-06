# pylint: disable-all
# type: ignore
# import numpy as np

# from src.structures import BinomialHeap


# def test_binomial_heap() -> None:
#     # Create a random permutation of 30 integers to be inserted and 19 of them deleted
#     permutation = np.random.permutation(list(range(30)))

#     # Create a Heap and insert the 30 integers
#     first_heap = BinomialHeap()
#     for number in permutation:
#         first_heap.insert(number)

#     assert first_heap.size == 30

#     for i in range(25):
#         assert first_heap.delete_min() == i

#     second_heap = BinomialHeap()
#     vals = [17, 20, 31, 34]
#     for value in vals:
#         second_heap.insert(value)

#     # The heap should have the following structure:
#     #   17
#     #  /  \
#     # #    31
#     #     /  \
#     #  20    34
#     # /  \  /  \
#     # #    # #   #

#     assert second_heap.pre_order() == [
#         (17, 0),
#         ("#", 1),
#         (31, 1),
#         (20, 2),
#         ("#", 3),
#         ("#", 3),
#         (34, 2),
#         ("#", 3),
#         ("#", 3),
#     ]

#     assert str(second_heap) == (
#         "17\n" "-#\n" "-31\n" "--20\n" "---#\n" "---#\n" "--34\n" "---#\n" "---#"
#     )

#     merged = second_heap.merge_heaps(first_heap)
#     assert merged.peek() == 17

#     # values in merged heap; (merge is inplace)
#     expected = [17, 20, 25, 26, 27, 28, 29, 31, 34]
#     while not first_heap.is_empty():
#         assert first_heap.delete_min() == expected.pop(0)


# class BinomialHeapTest(unittest.TestCase):
#     def test_size_1(self):
#         h = binomialheap.BinomialHeap()
#         h.enqueue(3)
#         h.check_structure()
#         self.assertEqual(1, len(h))
#         self.assertEqual(3, h.peek())
#         self.assertEqual(3, h.dequeue())
#         h.check_structure()
#         self.assertEqual(0, len(h))

#     def test_size_2(self):
#         h = binomialheap.BinomialHeap()
#         h.enqueue(4)
#         h.enqueue(2)
#         h.check_structure()
#         self.assertEqual(2, len(h))
#         self.assertEqual(2, h.peek())
#         self.assertEqual(2, h.dequeue())
#         h.check_structure()
#         self.assertEqual(1, len(h))
#         self.assertEqual(4, h.peek())
#         self.assertEqual(4, h.dequeue())
#         h.check_structure()
#         self.assertEqual(0, len(h))

#     def test_size_7(self):
#         h = binomialheap.BinomialHeap()
#         h.enqueue(2)
#         h.enqueue(7)
#         h.enqueue(1)
#         h.enqueue(8)
#         h.enqueue(3)
#         h.check_structure()
#         h.enqueue(1)
#         h.enqueue(4)
#         h.check_structure()
#         self.assertEqual(7, len(h))
#         self.assertEqual(1, h.dequeue())
#         self.assertEqual(6, len(h))
#         self.assertEqual(1, h.dequeue())
#         self.assertEqual(5, len(h))
#         self.assertEqual(2, h.dequeue())
#         self.assertEqual(4, len(h))
#         self.assertEqual(3, h.dequeue())
#         self.assertEqual(3, len(h))
#         h.check_structure()
#         self.assertEqual(4, h.dequeue())
#         self.assertEqual(2, len(h))
#         self.assertEqual(7, h.dequeue())
#         self.assertEqual(1, len(h))
#         self.assertEqual(8, h.dequeue())
#         self.assertEqual(0, len(h))
#         h.check_structure()

#     def test_against_list_randomly(self):
#         TRIALS = 1000
#         MAX_SIZE = 300
#         RANGE = 1000

#         heap = binomialheap.BinomialHeap()
#         for _ in range(TRIALS):
#             size = random.randrange(MAX_SIZE)
#             values = [random.randrange(RANGE) for _ in range(size)]
#             for val in values:
#                 heap.enqueue(val)

#             values.sort()
#             for val in values:
#                 self.assertEqual(val, heap.dequeue())

#             self.assertTrue(heap.empty())
#             heap.clear()

#     def test_against_python_priority_queue_randomly(self):
#         TRIALS = 10000
#         ITER_OPS = 100
#         RANGE = 10000

#         que = queue.PriorityQueue()
#         heap = binomialheap.BinomialHeap()
#         size = 0
#         for i in range(TRIALS):
#             if i % 300 == 0:
#                 print(f"Progress: {i / TRIALS:.0%}")
#             op = random.randrange(100)

#             if op < 1:  # Clear
#                 heap.check_structure()
#                 for _ in range(size):
#                     self.assertEqual(heap.dequeue(), que.get(False))
#                 size = 0

#             elif op < 2:  # Peek
#                 heap.check_structure()
#                 if size > 0:
#                     val = que.get(False)
#                     self.assertEqual(heap.peek(), val)
#                     que.put(val)

#             elif op < 70:  # Enqueue/merge
#                 merge = not op < 60
#                 sink = binomialheap.BinomialHeap() if merge else heap
#                 n = random.randint(1, ITER_OPS)
#                 for _ in range(n):
#                     val = random.randrange(RANGE)
#                     que.put(val)
#                     sink.enqueue(val)
#                 if merge:
#                     heap.merge(sink)
#                     self.assertEqual(len(sink), 0)
#                 size += n

#             elif op < 100:  # Dequeue
#                 n = min(random.randint(1, ITER_OPS), size)
#                 for _ in range(n):
#                     self.assertEqual(heap.dequeue(), que.get(False))
#                 size -= n

#             else:
#                 raise AssertionError()

#             self.assertEqual(que.qsize(), size)
#             self.assertEqual(len(heap), size)
#             self.assertEqual(que.empty(), size == 0)
#             self.assertEqual(heap.empty(), size == 0)


# if __name__ == "__main__":
#     unittest.main()
