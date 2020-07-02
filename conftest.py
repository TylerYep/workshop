from typing import Tuple

import numpy as np
import pytest
from torchvision import datasets


@pytest.fixture(scope="session")
def fashion_mnist(num_train: int = 5000, num_test: int = 500) -> Tuple[np.ndarray, ...]:
    train_set = datasets.FashionMNIST("data/", train=True, download=True)
    test_set = datasets.FashionMNIST("data/", train=False, download=True)

    X_train, y_train = train_set.data.numpy(), train_set.targets.numpy()
    X_test, y_test = test_set.data.numpy(), test_set.targets.numpy()

    mask = list(range(num_train))
    X_train = X_train[mask]
    y_train = y_train[mask]

    mask = list(range(num_test))
    X_test = X_test[mask]
    y_test = y_test[mask]

    X_train = np.reshape(X_train, (num_train, -1))
    X_test = np.reshape(X_test, (num_test, -1))

    return X_train, y_train, X_test, y_test
