import os
import pprint

IGNORED_FOLDERS = ("rmq", "sort", "hash_table", "conversions", "ml")
IGNORED_FILES = "util.py"


def test_file_coverage() -> None:
    untested_files = []
    for root, _, files in os.walk("src"):
        if os.path.basename(root) in IGNORED_FOLDERS:
            continue
        new_root = root.replace("src", "tests")
        for filename in files:
            if filename in IGNORED_FILES:
                continue
            basename, ext = os.path.splitext(filename)
            if ext == ".py" and "__" not in filename:
                partner = os.path.join(new_root, basename + "_test.py")
                if not os.path.isfile(partner):
                    untested_files.append((os.path.join(root, filename), partner))
    assert not untested_files, pprint.pformat(untested_files)
