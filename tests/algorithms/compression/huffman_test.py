from pathlib import Path

from cs.algorithms import huffman_compress, huffman_decompress
from cs.algorithms.compression.huffman import HuffmanTreeNode


def test_huffman(tmp_path: Path) -> None:
    file_to_compress = Path("cs/algorithms/compression/huffman.py")
    compressed_file_name = tmp_path / "output.huf"

    tree = huffman_compress(file_to_compress, compressed_file_name)

    leftmost = tree
    while leftmost.left is not None:
        leftmost = leftmost.left

    assert leftmost == HuffmanTreeNode(freq=40, letter=")")
    assert repr(leftmost) == "HuffmanTreeNode(freq=40, letter=')', bitstring='000000')"

    output = huffman_decompress(compressed_file_name, tree)

    assert file_to_compress.read_text() == output
