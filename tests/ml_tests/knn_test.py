from typing import Tuple

import numpy as np
import pytest

from src.ml.knn import KNearestNeighbors


@pytest.mark.skip(reason="Takes ~0.3 seconds to run")  # type: ignore[misc]
def test_knn_compute_distance(fashion_mnist: Tuple[np.ndarray, ...]) -> None:
    X_train, y_train, X_test, _ = fashion_mnist

    knn = KNearestNeighbors(X_train, y_train)

    distsA = knn.compute_distances(X_test, 0)
    distsB = knn.compute_distances(X_test, 1)
    assert np.linalg.norm(distsA - distsB) < 0.001


# def test_knn_predict_labels(fashion_mnist) -> None:
#     pass
