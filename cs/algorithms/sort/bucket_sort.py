BUCKET_SIZE = 10


def bucket_sort(array: list[int]) -> list[int]:
    """
    Time Complexity of Solution:
    Worst Case: occurs when all the elements are placed in a single bucket.
    The overall performance would then be dominated by the algorithm used to sort each
    bucket. In this case, O(n log n), because of TimSort.

    Average Case: O(n + (n^2)/k + k), where k is the number of buckets.
    If k = O(n), time complexity is O(n).

    Runtime: O(n)
    """
    if not array:
        return array
    min_value, max_value = min(array), max(array)
    bucket_count = (max_value - min_value) // BUCKET_SIZE + 1
    buckets: list[list[int]] = [[] for _ in range(int(bucket_count))]

    for item in array:
        buckets[int((item - min_value) // BUCKET_SIZE)].append(item)

    return sorted(
        buckets[i][j] for i in range(len(buckets)) for j in range(len(buckets[i]))
    )
