import os
import pprint
from types import ModuleType

IGNORED_FOLDERS = {"rmq", "sort", "hash_table", "heap", "conversions"}
IGNORED_FILES = {"util.py", "svm.py", "linear_classifier.py", "softmax.py"}
SRC_FOLDER = "src"
TEST_FOLDER = "tests"


def test_file_coverage() -> None:
    untested_files = []
    if not os.path.isdir(SRC_FOLDER) or not os.path.isdir(SRC_FOLDER):
        raise RuntimeError(f"{SRC_FOLDER} and/or {TEST_FOLDER} does not exist.")
    for root, _, files in os.walk(SRC_FOLDER):
        if set(os.path.normpath(root).split(os.sep)) & IGNORED_FOLDERS:
            continue
        new_root = root.replace(SRC_FOLDER, TEST_FOLDER)
        for filename in files:
            if filename in IGNORED_FILES:
                continue
            basename, ext = os.path.splitext(filename)
            if ext == ".py" and "__" not in filename:
                partner = os.path.join(new_root, basename + "_test.py")
                if not os.path.isfile(partner):
                    untested_files.append((os.path.join(root, filename), partner))
    assert not untested_files, pprint.pformat(untested_files)


def test_all_exported() -> None:
    """ Test that __all__ contains only names that are actually exported. """
    import src.algorithms as algorithms
    import src.maths as maths
    import src.structures as structures

    for module in (algorithms, maths, structures):
        if hasattr(module, "__all__"):
            module_all = module.__all__  # type: ignore[attr-defined]
            missing_export = [name for name in module_all if not hasattr(module, name)]
            extra_exports = [
                name
                for name in dir(module)
                if "__" not in name
                and not isinstance(getattr(module, name), ModuleType)
                and name not in module_all
            ]

            assert not missing_export
            assert not extra_exports
