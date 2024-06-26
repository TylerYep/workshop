from pathlib import Path

from cs.algorithms import huffman_compress, huffman_decompress
from cs.algorithms.compression.huffman import HuffmanTreeNode


def test_huffman(tmp_path: Path) -> None:
    """Note that if the source file changes, this test output needs to be updated."""
    file_to_compress = Path("cs/algorithms/compression/huffman.py")
    compressed_file_name = tmp_path / "output.huf"

    tree = huffman_compress(file_to_compress, compressed_file_name)

    leftmost = tree
    while leftmost.left is not None:
        leftmost = leftmost.left

    assert leftmost == HuffmanTreeNode(freq=41, letter="(")
    assert repr(leftmost) == (
        "HuffmanTreeNode(freq=41, letter='(', bitstring='000000')"
    )

    output = huffman_decompress(compressed_file_name, tree)

    assert file_to_compress.read_text(encoding="utf-8") == output
