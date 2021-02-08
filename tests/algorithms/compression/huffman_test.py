import os

from cs.algorithms import huffman_compress, huffman_decompress
from cs.algorithms.compression.huffman import HuffmanTreeNode


def test_huffman(tmp_path: str) -> None:
    file_to_compress = "cs/algorithms/compression/huffman.py"
    compressed_file_name = os.path.join(tmp_path, "output.huf")

    tree = huffman_compress(file_to_compress, compressed_file_name)

    leftmost = tree
    while leftmost.left is not None:
        leftmost = leftmost.left
    expected = HuffmanTreeNode(freq=19, letter="T", bitstring="0000000")

    assert leftmost == expected
    assert repr(leftmost) == "HuffmanTreeNode(freq=19, letter='T', bitstring='0000000')"

    output = huffman_decompress(compressed_file_name, tree)

    with open(file_to_compress) as f:
        assert f.read() == output
