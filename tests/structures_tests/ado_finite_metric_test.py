import random

import numpy as np

from src.structures.ado_finite_metric import ApproxFiniteMetricOracle


def test_zero_distance_approx() -> None:
    random.seed(0)
    distance_matrix = np.zeros((4, 4))

    ado = ApproxFiniteMetricOracle(distance_matrix)

    assert ado.query(0, 2) == 0
    assert ado.query(3, 2) == 0


def test_approx_greater_than_actual() -> None:
    random.seed(0)
    distance_matrix = np.ones((41, 41))
    distance_matrix[0, 40] = 50
    distance_matrix[40, 0] = 50

    ado = ApproxFiniteMetricOracle(distance_matrix)

    assert ado.query(3, 5) == 2.0
    assert ado.query(0, 3) == 51.0
    assert ado.query(0, 30) == 51.0
