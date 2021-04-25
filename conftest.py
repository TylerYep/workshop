import inspect
import random
import time
from collections.abc import Callable
from typing import Any

# import numpy as np
import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Node


@pytest.fixture(autouse=True)
def _set_random_seed(seed: int = 0) -> None:
    random.seed(seed)
    # np.random.seed(seed)


def assert_a_faster_than_b(
    variant_a: Callable[..., Any],
    variant_b: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> None:
    start = time.perf_counter()
    variant_a(*args, **kwargs)
    end = time.perf_counter()
    fast_version = end - start

    start = time.perf_counter()
    variant_b(*args, **kwargs)
    end = time.perf_counter()
    slow_version = end - start

    assert fast_version < slow_version, f"{fast_version} {slow_version}"


def add_fixtures(metafunc: Any, *fixture_names: str) -> None:
    """Used for linking fixtures in class vars to the inherited superclass."""
    for name in fixture_names:
        if name in inspect.signature(metafunc.function).parameters:
            metafunc.parametrize(name, [getattr(metafunc.cls, name)])


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--runslow", action="store_true")


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config: Config, items: list[Node]) -> None:
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run this test")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
