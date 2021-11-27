import inspect
import random
import time
from collections.abc import Callable
from typing import Any

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Node
from _pytest.python import Metafunc


@pytest.fixture(autouse=True)
def _set_random_seed(seed: int = 0) -> None:
    random.seed(seed)


def pytest_configure(config: Config) -> None:
    config.addinivalue_line(
        "markers",
        (
            "add_function(*args): Used for linking functions stored in class vars "
            "to the fixtures of the inherited test class."
        ),
    )


def pytest_generate_tests(metafunc: Metafunc) -> None:
    marker = metafunc.definition.get_closest_marker("add_function")
    if marker is not None:
        for function_name in marker.args:
            if function_name in inspect.signature(metafunc.function).parameters:
                metafunc.parametrize(
                    function_name, [getattr(metafunc.cls, function_name)]
                )


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--runslow", action="store_true")


def pytest_collection_modifyitems(config: Config, items: list[Node]) -> None:
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run this test")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


def pytest_idempotent_decorator() -> str:
    return "cs.util.idempotent"


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
