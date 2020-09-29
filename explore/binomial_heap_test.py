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
