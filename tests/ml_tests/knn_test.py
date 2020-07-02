import numpy as np

from src.ml.knn import KNearestNeighbors


def test_knn_compute_distance(fashion_mnist):
    X_train, y_train, X_test, y_test = fashion_mnist

    knn = KNearestNeighbors(X_train, y_train)

    distsA = knn.compute_distances(X_test, 0)
    distsB = knn.compute_distances(X_test, 1)
    assert np.linalg.norm(distsA - distsB) < 0.001


def test_knn_predict_labels(fashion_mnist):
    pass
