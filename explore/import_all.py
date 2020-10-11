import re
import sys
from typing import Tuple


def create_all_exports(init_file_content: str) -> Tuple[str]:
    file_parts = init_file_content.split("\n")
    matches = []
    reg = re.compile("from .* import ")
    for line in file_parts:
        if match := reg.search(line):
            matches.append(line[match.end() :])

    exports = []
    for result in matches:
        split_on_commas = result.split(", ")
        for i, split in enumerate(split_on_commas):
            if (index := split.find(" as ")) != -1:
                split_on_commas[i] = split_on_commas[i][index + len(" as ") :]
        exports.extend(split_on_commas)
    return f"__all__ = {tuple(exports)}"


if __name__ == "__main__":
    # init_file_content = (
    #     "from .binary import binary_search, left_right_binary_search, linear_search\n"
    #     "from .comp.huffman import huffman_compress, as\n"
    #     "from .grass import breadth_first_search\n"
    #     "from .str import lcs\n"
    #     "from .str import build_suffix_array_sais as build_suffix_array\n"
    # )
    # result = create_all_exports(init_file_content)
    # assert len(result) == 8
    # print(result)

    with open(sys.argv[1]) as f:
        content = f.read()
        print(create_all_exports(content))
