"""
https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform

The Burrows–Wheeler transform (BWT, also called block-sorting compression)
rearranges a character string into runs of similar characters. This is useful
for compression, since it tends to be easy to compress a string that has runs
of repeated characters by techniques such as move-to-front transform and
run-length encoding. More importantly, the transformation is reversible,
without needing to store any additional data except the position of the first
original character. The BWT is thus a "free" method of improving the efficiency
of text compression algorithms, costing only some extra computation.
"""


def all_rotations(s: str) -> list[str]:
    """
    :param s: The string that will be rotated len(s) times.
    :return: A list with the rotations.
    """
    return [s[i:] + s[:i] for i in range(len(s))]


def bwt_transform(s: str) -> tuple[str, int]:
    """
    :param s: The string that will be used at bwt algorithm
    :return: the string composed of the last char of each row of the ordered
    rotations and the index of the original string at ordered rotations list
    """
    rotations = sorted(all_rotations(s))
    return "".join([word[-1] for word in rotations]), rotations.index(s)


def reverse_bwt(bwt_string: str, idx_original_string: int) -> str:
    """
    :param bwt_string: The string returned from bwt algorithm execution
    :param idx_original_string: A 0-based index of the string that was used to
    generate bwt_string at ordered rotations list
    :return: The string used to generate bwt_string when bwt was executed
    """
    if not bwt_string or not 0 <= idx_original_string < len(bwt_string):
        raise RuntimeError("Invalid input to reverse_bwt")

    ordered_rotations = [""] * len(bwt_string)
    for _ in range(len(bwt_string)):
        for i, bwt in enumerate(bwt_string):
            ordered_rotations[i] = bwt + ordered_rotations[i]
        ordered_rotations.sort()
    return ordered_rotations[idx_original_string]
