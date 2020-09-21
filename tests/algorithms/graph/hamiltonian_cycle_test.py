from src.algorithms import hamiltonian_cycle


def test_hamiltonian_cycle() -> None:
    # This graph contains multiple Hamiltonian cycles,
    # for example: (0)->(1)->(2)->(4)->(3)->(0)
    # (0)---(1)---(2)
    #  |   /   \   |
    #  |  /     \  |
    #  | /       \ |
    #  |/         \|
    # (3)---------(4)
    graph = [
        [0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1],
        [0, 1, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ]
    assert hamiltonian_cycle(graph, 0) == [0, 1, 2, 4, 3, 0]
    assert hamiltonian_cycle(graph, 2) == [2, 1, 0, 3, 4, 2]
    assert hamiltonian_cycle(graph, 3) == [3, 0, 1, 2, 4, 3]

    graph = [
        [0, 1, 0, 1, 0],
        [1, 0, 1, 1, 1],
        [0, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
    ]

    # Following Graph is exactly what it was before, but edge 3-4 is removed.
    # Result is that there is no Hamiltonian Cycle anymore.
    # (0)---(1)---(2)
    #  |   /   \   |
    #  |  /     \  |
    #  | /       \ |
    #  |/         \|
    # (3)         (4)
    assert hamiltonian_cycle(graph, 4) == []
