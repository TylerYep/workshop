from __future__ import annotations

import pprint
from pathlib import Path
from types import ModuleType

IGNORED_FOLDERS = {"__pycache__"}
IGNORED_FILES = {"__init__.py", "util.py"}
SRC_FOLDER = Path("cs")
TEST_FOLDER = Path("tests")


def test_file_coverage() -> None:
    """Test that all files in cs/ have a corresponding file in tests/."""
    untested_files: list[str | tuple[str, str]] = []
    if not SRC_FOLDER.is_dir() or not TEST_FOLDER.is_dir():
        raise RuntimeError(f"{SRC_FOLDER} and/or {TEST_FOLDER} does not exist.")
    for filepath in SRC_FOLDER.rglob("*.py"):
        if (
            filepath.name not in IGNORED_FILES
            and not set(filepath.parts) & IGNORED_FOLDERS
        ):
            partner = TEST_FOLDER / filepath.relative_to(SRC_FOLDER)
            partner_parent = partner.parent
            if not partner_parent.is_dir():
                # Some folders only use a single test file.
                parent_test = (partner_parent.parent / partner_parent.name).with_stem(
                    f"{partner_parent.name}_test.py"
                )
                if not parent_test.is_file():
                    untested_files.append(str(parent_test))
                continue
            partner = partner.with_stem(f"{partner.stem}_test")
            if not partner.is_file():
                untested_files.append((str(filepath), str(partner)))
    assert not untested_files, pprint.pformat(untested_files)


def test_all_exported() -> None:
    """Test that __all__ contains only names that are actually exported."""
    from cs import algorithms, maths, structures

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
