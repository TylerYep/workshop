from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

from cs.util import dfield


@dataclass(order=True, slots=True)
class HuffmanTreeNode:
    freq: int
    letter: str = field(default="")
    left: HuffmanTreeNode | None = dfield(None)
    right: HuffmanTreeNode | None = dfield(None)
    bitstring: str = field(default="", compare=False)


def parse_file(filepath: Path) -> list[HuffmanTreeNode]:
    """
    Read the file and build a dict of all letters and their
    frequencies, then convert the dict into a list of Letters.
    """
    chars: dict[str, int] = {}
    with open(filepath, encoding="utf-8") as f:
        while c := f.read(1):
            if c in chars:
                chars[c] += 1
            else:
                chars[c] = 1

    queue = [HuffmanTreeNode(freq, ch) for ch, freq in chars.items()]
    heapq.heapify(queue)
    return queue


def build_tree(letters: list[HuffmanTreeNode]) -> HuffmanTreeNode:
    """
    Run through the list of Letters and build the
    min heap for the Huffman Tree.
    """
    while len(letters) > 1:
        left = heapq.heappop(letters)
        right = heapq.heappop(letters)
        node = HuffmanTreeNode(left.freq + right.freq, left=left, right=right)
        heapq.heappush(letters, node)
    return letters[0]


def encode(root: HuffmanTreeNode, bitstring: str) -> list[HuffmanTreeNode]:
    """
    Recursively traverse the Huffman Tree to set each
    letter's bitstring, and return the list of letters.
    """
    if root.left is None or root.right is None:
        root.bitstring = bitstring
        return [root]
    return encode(root.left, bitstring + "0") + encode(root.right, bitstring + "1")


def huffman_compress(
    filepath: Path, output_filepath: Path | None = None
) -> HuffmanTreeNode:
    """
    Parse the file, build the tree, then run through the file
    again, using the list of Letters to find and print out the
    bitstring for each letter.
    """
    # print(f"Huffman Coding of {filepath}: ")
    queue = parse_file(filepath)
    root = build_tree(queue)
    letters = encode(root, "")

    encoding = ""
    with open(filepath, encoding="utf-8") as f:
        while c := f.read(1):
            [byte] = [letter for letter in letters if letter.letter == c]
            encoding += byte.bitstring

    output_path = (
        filepath.with_suffix(".huf") if output_filepath is None else output_filepath
    )
    output_path.write_text(encoding, encoding="utf-8")
    return root


def decode(root: HuffmanTreeNode, filepath: Path) -> str:
    """
    Recursively traverse the Huffman Tree to read each
    letter in the bitstring, and return the decoded string of letters.
    """
    output = ""
    curr = root
    with open(filepath, encoding="utf-8") as f:
        while bit := f.read(1):
            if bit not in ("0", "1"):
                raise ValueError(
                    f"Input bitstring contained character other than 0 or 1: {bit}"
                )
            if curr.letter:
                output += curr.letter
                curr = root
            if bit == "0":
                curr = cast(HuffmanTreeNode, curr.left)
            elif bit == "1":
                curr = cast(HuffmanTreeNode, curr.right)
    output += curr.letter
    return output


def huffman_decompress(filepath: Path, root: HuffmanTreeNode) -> str:
    """
    Parse the file, then use the input to find and print
    out the letter for each bitstring.
    """
    output = decode(root, filepath)
    # print(f"Huffman Decoding of {filepath}: {output}")
    return output
