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
        if mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


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
        else:
            right = mid - 1
    return index
