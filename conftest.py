import random
import time
from typing import Any, Callable, List, Tuple

import numpy as np
import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Node
from torchvision import datasets


@pytest.fixture(autouse=True)
def set_random_seed(seed: int = 0) -> None:
    random.seed(seed)
    np.random.seed(seed)


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


@pytest.fixture(scope="session")
def fashion_mnist(num_train: int = 100, num_test: int = 10) -> Tuple[np.ndarray, ...]:
    train_set = datasets.FashionMNIST("data/", train=True, download=True)
    test_set = datasets.FashionMNIST("data/", train=False, download=True)

    X_train, y_train = train_set.data.numpy().astype(float), train_set.targets.numpy()
    X_test, y_test = test_set.data.numpy().astype(float), test_set.targets.numpy()

    mask = list(range(num_train))
    X_train = X_train[mask]
    y_train = y_train[mask]

    mask = list(range(num_test))
    X_test = X_test[mask]
    y_test = y_test[mask]

    mean_image = np.mean(X_train, axis=0)
    X_train -= mean_image
    X_test -= mean_image

    X_train = np.reshape(X_train, (num_train, -1))
    X_test = np.reshape(X_test, (num_test, -1))

    return X_train, y_train, X_test, y_test


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--runslow", action="store_true", default=False)


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config: Config, items: List[Node]) -> None:
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run this test")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
