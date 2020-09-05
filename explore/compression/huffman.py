from __future__ import annotations

import heapq
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(order=True)
class HuffmanTreeNode:
    freq: int
    left: Optional[HuffmanTreeNode] = field(default=None, compare=False)
    right: Optional[HuffmanTreeNode] = field(default=None, compare=False)
    letter: str = field(default="", compare=False)
    bitstring: str = field(default="", compare=False)


def parse_file(file_path: str) -> List[HuffmanTreeNode]:
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


def build_tree(letters: List[HuffmanTreeNode]) -> HuffmanTreeNode:
    """ Run through the list of Letters and build the min heap for the Huffman Tree. """
    while len(letters) > 1:
        left = heapq.heappop(letters)
        right = heapq.heappop(letters)
        node = HuffmanTreeNode(left.freq + right.freq, left, right)
        heapq.heappush(letters, node)
    return letters[0]


def traverse_tree(root: HuffmanTreeNode, bitstring: str) -> List[HuffmanTreeNode]:
    """
    Recursively traverse the Huffman Tree to set each
    letter's bitstring, and return the list of letters.
    """
    if root.left is None or root.right is None:
        root.bitstring = bitstring
        return [root]
    return traverse_tree(root.left, bitstring + "0") + traverse_tree(root.right, bitstring + "1")


def compress(file_path: str) -> None:
    """
    Parse the file, build the tree, then run through the file
    again, using the list of Letters to find and print out the
    bitstring for each letter.
    """
    letters_list = parse_file(file_path)
    root = build_tree(letters_list)
    letters = traverse_tree(root, "")
    print(f"Huffman Coding of {file_path}: ")
    with open(file_path) as f:
        while c := f.read(1):
            byte = list(filter(lambda l: l.letter == c, letters))[0]
            print(byte.bitstring, end=" ")


if __name__ == "__main__":
    compress(sys.argv[1])
