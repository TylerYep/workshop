from collections import Counter
from dataclasses import dataclass
from enum import Enum, unique


@unique
class SuffixType(Enum):
    S, L = "S", "L"


@dataclass(slots=True)
class LMSBlock:
    start: int
    end: int
    block_num: int = -1


def build_suffix_array_naive(source: str) -> list[int]:
    """
    A naive, slow suffix-array construction algorithm.
    Construct a list of suffixes of the source string, then calculate the start
    offset of each suffix, storing them in sorted order into the suffix array.

    Runtime: O(n log n)
    """
    n = len(source)
    suffixes = sorted(source[offset:] for offset in range(n + 1))
    return [n - len(suffix) for suffix in suffixes]


def build_suffix_array(orig_text: str) -> list[int]:
    """
    SAIS algorithm to form a Suffix Array.

    Runtime: O(n)
    """

    def _sais(text: list[int]) -> list[int]:
        """Helper function required to handle the recursive call."""

        # Handle empty string edge case
        if not orig_text:
            return [0]

        # Step 1: Annotate all suffixes as L/S and get LMS suffixes.
        suffix_marks, lms_suffixes = get_suffix_annotations(text)

        # Step 2: Run Induced sorting on the suffix array.
        suffix_arr = induced_sort(text, suffix_marks, lms_suffixes)

        # Step 3: Get the reduced string.
        reduced_str, should_recurse = get_reduced_string(text, suffix_arr, lms_suffixes)

        # Step 4: Sort the reduced string by computing its suffix array!
        if should_recurse:
            reduced_suffix_arr = _sais(reduced_str)
        else:
            reduced_suffix_arr = [-1] * len(reduced_str)
            for i, item in enumerate(reduced_str):
                reduced_suffix_arr[item] = i

        sorted_lms_suffixes = reorder_lms_substrings(lms_suffixes, reduced_suffix_arr)

        # Step 5: Final induced sorting pass.
        return induced_sort(text, suffix_marks, sorted_lms_suffixes)

    # Step 0: Convert text to rank array.
    return _sais(to_rank_array(orig_text))


def create_lms_blocks(
    suffix_arr: list[int], lms_suffixes: list[int]
) -> tuple[list[LMSBlock], dict[int, int]]:
    """
    This function fetches all LMS blocks, which span from one LMS suffix to another.
    """
    # Stores the index in the original lms_suffix list.
    is_lms_suffix = [-1] * len(suffix_arr)
    for index, suffix in enumerate(lms_suffixes):
        is_lms_suffix[suffix] = index
    sorted_lms_suffixes = [item for item in suffix_arr if is_lms_suffix[item] != -1]

    lms_blocks = []
    block_mapping = {}
    for i, curr_suffix in enumerate(sorted_lms_suffixes):
        search = is_lms_suffix[curr_suffix] + 1
        next_suffix = (
            curr_suffix if search == len(lms_suffixes) else lms_suffixes[search]
        )
        lms_blocks.append(LMSBlock(curr_suffix, next_suffix))
        block_mapping[curr_suffix] = i
    return lms_blocks, block_mapping


def assign_block_numbers(text: list[int], lms_blocks: list[LMSBlock]) -> bool:
    """
    Iterate over the sorted LMS blocks and assign them block numbers in place. If any
    two have the same block number, make a note to recurse later to sort the
    LMS suffixes. We assume that lmsBlocks is in sorted order by appearance in text.
    """
    lms_blocks[0].block_num = 0
    curr_block = 1
    should_recurse = False
    for i in range(1, len(lms_blocks)):
        block = lms_blocks[i]
        prev_block = lms_blocks[i - 1]
        if (
            text[block.start : block.end + 1]
            == text[prev_block.start : prev_block.end + 1]
        ):
            block.block_num = prev_block.block_num
            should_recurse = True
        else:
            block.block_num = curr_block
            curr_block += 1
    return should_recurse


def get_reduced_string(
    text: list[int], suffix_arr: list[int], lms_suffixes: list[int]
) -> tuple[list[int], bool]:
    """
    >>> suffix_arr = [10, 0, 1, 2, 3, 4, 6, 8, 5, 7, 9]
    >>> lms_suffixes = [6, 8, 10]
    >>> get_reduced_string("AAAAACACAG", suffix_arr, lms_suffixes)
    ([1, 2, 0], False)
    """
    lms_blocks, block_mapping = create_lms_blocks(suffix_arr, lms_suffixes)
    should_recurse = assign_block_numbers(text, lms_blocks)

    reduced_str = []
    for suffix in lms_suffixes:
        block_index = block_mapping[suffix]
        reduced_str.append(lms_blocks[block_index].block_num)
    return reduced_str, should_recurse


def reorder_lms_substrings(
    lms_suffixes: list[int], reduced_str: list[int]
) -> list[int]:
    """
    >>> reorder_lms_substrings([2, 6, 8, 11, 13, 16, 20], [6, 5, 3, 1, 0, 4, 2])
    [20, 16, 11, 6, 2, 13, 8]
    """
    return [lms_suffixes[reduced_str[i]] for i in range(len(reduced_str))]


def induced_sort(
    text: list[int], suffix_marks: list[SuffixType], lms_suffixes: list[int]
) -> list[int]:
    """
    Runs induced sort on the text and returns a suffix array.
    """
    alphabet_size = max(text)
    suffix_arr = [-1] * len(text)

    histogram = Counter(text)
    bucket_starts = [0] * (alphabet_size + 1)  # text -> start ind
    bucket_ends = list(bucket_starts)

    for i in range(1, alphabet_size + 1):
        bucket_starts[i] = bucket_starts[i - 1] + histogram[i - 1]
        bucket_ends[i] = bucket_ends[i - 1] + histogram[i]

    orig_bucket_ends = list(bucket_ends)

    # Make backward pass and insert all LMS suffixes into their
    # proper places at the bucket ends.
    for lms_suffix in reversed(lms_suffixes):
        bucket = bucket_ends[text[lms_suffix]]
        suffix_arr[bucket] = lms_suffix
        bucket_ends[text[lms_suffix]] -= 1

    # Make forward pass and insert all L-type suffixes
    # into the proper places at the bucket starts.
    for key in suffix_arr:
        if key > 0:
            ind = key - 1
            if suffix_marks[ind] == SuffixType.L:
                bucket = bucket_starts[text[ind]]
                suffix_arr[bucket] = ind
                bucket_starts[text[ind]] += 1

    # Make final backward pass and reinsert all S-type suffixes into the proper
    # places at the bucket ends, overwriting any previously placed suffixes.
    bucket_ends = orig_bucket_ends
    for i in range(len(suffix_arr) - 1, 0, -1):
        key = suffix_arr[i]
        if key > 0:
            ind = key - 1
            if suffix_marks[ind] is SuffixType.S:
                bucket = bucket_ends[text[ind]]
                suffix_arr[bucket] = ind
                bucket_ends[text[ind]] -= 1

    return suffix_arr


def get_suffix_annotations(text: list[int]) -> tuple[list[SuffixType], list[int]]:
    """
    Returns all LMS suffixes, as well as the L/S markings for each index.
    >>> marks, lms = get_suffix_annotations("ACGTGCCTAGCCTACCGTGCC$")
    >>> [x.value for x in marks]  # doctest: +NORMALIZE_WHITESPACE
    ['S', 'S', 'S', 'L', 'L', 'S', 'S', 'L', 'S', 'L', 'S',
     'S', 'L', 'S', 'S', 'S', 'S', 'L', 'L', 'L', 'L', 'S']
    >>> lms
    [5, 8, 10, 13, 21]
    """
    lms_suffixes: list[int] = []
    suffix_marks = [SuffixType.S] * len(text)
    for k in range(len(text) - 1, 0, -1):
        if (
            text[k - 1] > text[k]
            or text[k - 1] == text[k]
            and suffix_marks[k] is SuffixType.L
        ):
            suffix_marks[k - 1] = SuffixType.L
            if suffix_marks[k] is SuffixType.S:
                lms_suffixes.append(k)

    lms_suffixes.reverse()
    return suffix_marks, lms_suffixes


def to_rank_array(text: str) -> list[int]:
    """
    Gets rank array representation for a text. Appends a sentinel $ at the end.
    >>> to_rank_array("abracadabra")
    [1, 2, 5, 1, 3, 1, 4, 1, 2, 5, 1, 0]
    >>> to_rank_array("ACGTGCCTAGCCTACCGTGCC")
    [1, 2, 3, 4, 3, 2, 2, 4, 1, 3, 2, 2, 4, 1, 2, 2, 3, 4, 3, 2, 2, 0]
    """
    chars = sorted(set(text))
    char_map: dict[str, int] = {}
    for ch in chars:
        char_map[ch] = len(char_map) + 1
    result: list[int] = []
    for ch in text:
        result.append(char_map[ch])
    # End string terminator
    result.append(0)
    return result


def rank_text_to_str(char_map: dict[str, int], rank_text: list[int]) -> str:
    """Util function to convert rank text back into strings."""
    result = ""
    reversed_char_map = {}
    reversed_char_map[0] = "$"
    for ch in char_map:
        reversed_char_map[char_map[ch]] = ch
    for num in rank_text:
        result += reversed_char_map[num]
    return result
