from typing import Any, List


def binary_search(nums: List[Any], target: int) -> int:
    """ Returns the index of target element, or -1 if it cannot be found. """
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        mid_val = nums[mid]
        if target == mid_val:
            return mid
        elif mid_val < target:
            left = mid + 1
        elif mid_val > target:
            right = mid - 1
    return -1


assert binary_search([0], target=0) == 0
assert binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8], target=1) == 1
assert binary_search([1, 2, 4, 5, 6, 7, 8], target=3) == -1
assert binary_search([1, 2, 3, 4, 5, 6, 7, 8], target=5) == 4
assert binary_search([1, 2, 3, 4, 5, 6, 7, 8], target=8) == 7
UPPER_BOUND = 800
nums = [z for z in range(0, UPPER_BOUND, 2)]
for x in range(0, UPPER_BOUND, 4):
    assert binary_search(nums, target=x) == x // 2
assert binary_search(nums, target=UPPER_BOUND + 1) == -1


def left_right_binary_search(nums: List[Any], target: int, is_left: bool = True) -> int:
    """
    Returns the leftmost index of target element, or -1 if it cannot be found.
    Returns rightmost index if is_left is False.
    Allows duplicates.
    """
    left = 0
    right = len(nums) - 1
    index = -1
    while left <= right:
        mid = left + (right - left) // 2
        mid_val = nums[mid]
        if mid_val == target:
            index = mid
            if is_left:
                right = mid - 1
            else:
                left = mid + 1
        elif mid_val < target:
            left = mid + 1
        elif mid_val > target:
            right = mid - 1
    return index


assert left_right_binary_search([0], target=0) == 0
assert left_right_binary_search([0, 1, 2, 3, 3, 3, 6, 7, 8], target=3) == 3
assert left_right_binary_search([5] * 20, target=5) == 0

assert left_right_binary_search([0], target=0, is_left=False) == 0
assert left_right_binary_search([0, 1, 2, 3, 3, 3, 6, 7, 8], target=3, is_left=False) == 5
assert left_right_binary_search([5] * 20, target=5, is_left=False) == 19
