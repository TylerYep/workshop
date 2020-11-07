from src.structures import ApproxFiniteMetricOracle


def test_zero_distance_approx() -> None:
    distance_matrix = [[0.0] * 4] * 4

    ado = ApproxFiniteMetricOracle(distance_matrix)

    assert ado.query(0, 2) == 0
    assert ado.query(3, 2) == 0


def test_approx_greater_than_actual() -> None:
    distance_matrix = [[1.0] * 41] * 41
    distance_matrix[0][40] = 50
    distance_matrix[40][0] = 50

    ado = ApproxFiniteMetricOracle(distance_matrix)

    assert ado.query(3, 5) == 2.0
    assert ado.query(0, 3) == 51.0
    assert ado.query(0, 30) == 51.0


def test_custom_graph() -> None:
    dist_matrix = [[0, 1, 0, 5], [1, 0, 0, 0], [0, 0, 0, 0], [5, 0, 0, 0]]
    distances = [[float(i) for i in row] for row in dist_matrix]
    ado = ApproxFiniteMetricOracle(distances)

    assert ado.query(0, 2) == 0.0
