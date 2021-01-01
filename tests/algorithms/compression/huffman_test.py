import os

from cs.algorithms import huffman_compress, huffman_decompress


def test_huffman(tmp_path: str) -> None:
    file_to_compress = "cs/algorithms/compression/huffman.py"
    compressed_file_name = os.path.join(tmp_path, "output.huf")

    tree = huffman_compress(file_to_compress, compressed_file_name)
    output = huffman_decompress(compressed_file_name, tree)

    with open(file_to_compress) as f:
        assert f.read() == output
