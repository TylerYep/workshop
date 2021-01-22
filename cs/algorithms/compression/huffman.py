from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Dict, Optional, cast

from dataslots import dataslots


@dataslots
@dataclass(order=True)
class HuffmanTreeNode:
    freq: int
    left: Optional[HuffmanTreeNode] = field(default=None, compare=False, repr=False)
    right: Optional[HuffmanTreeNode] = field(default=None, compare=False, repr=False)
    letter: str = field(default="")
    bitstring: str = field(default="", compare=False)


def parse_file(file_path: str) -> list[HuffmanTreeNode]:
    """
    Read the file and build a dict of all letters and their
    frequencies, then convert the dict into a list of Letters.
    """
    chars: Dict[str, int] = {}
    with open(file_path) as f:
        while c := f.read(1):
            if c in chars:
                chars[c] += 1
            else:
                chars[c] = 1

    queue = [HuffmanTreeNode(freq, letter=ch) for ch, freq in chars.items()]
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
        node = HuffmanTreeNode(left.freq + right.freq, left, right)
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
    file_path: str, output_file_path: Optional[str] = None
) -> HuffmanTreeNode:
    """
    Parse the file, build the tree, then run through the file
    again, using the list of Letters to find and print out the
    bitstring for each letter.
    """
    # print(f"Huffman Coding of {file_path}: ")
    queue = parse_file(file_path)
    root = build_tree(queue)
    letters = encode(root, "")

    encoding = ""
    with open(file_path) as f:
        while c := f.read(1):
            byte = list(filter(lambda l: l.letter == c, letters))[0]
            encoding += byte.bitstring

    output_path = file_path + ".huf" if output_file_path is None else output_file_path
    with open(output_path, "w") as f:
        f.write(encoding)
    return root


def decode(root: HuffmanTreeNode, file_path: str) -> str:
    """
    Recursively traverse the Huffman Tree to read each
    letter in the bitstring, and return the decoded string of letters.
    """
    output = ""
    curr = root
    with open(file_path) as f:
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


def huffman_decompress(file_path: str, root: HuffmanTreeNode) -> str:
    """
    Parse the file, then use the input to find and print
    out the letter for each bitstring.
    """
    output = decode(root, file_path)
    # print(f"Huffman Decoding of {file_path}: {output}")
    return output
