from typing import List


def radix_sort(array: List[int]) -> List[int]:
    if not array:
        return array
    max_element = max(array)
    place = 1
    while max_element // place > 0:
        # Apply counting sort to sort elements based on place value.
        output = [0] * len(array)
        count = [0] * 10

        # Calculate count of elements
        for item in array:
            count[(item // place) % 10] += 1

        # Calculate cummulative count
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Place the elements in sorted order
        i = len(array) - 1
        while i >= 0:
            index = array[i] // place
            output[count[index % 10] - 1] = array[i]
            count[index % 10] -= 1
            i -= 1

        # Move to the next place
        array = output
        place *= 10
    return array
