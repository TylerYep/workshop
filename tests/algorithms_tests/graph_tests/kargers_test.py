from src.algorithms import kargers
from src.structures import Graph


def test_kargers() -> None:
    # Adjacency list representation of this graph:
    # https://en.wikipedia.org/wiki/File:Single_run_of_Karger%E2%80%99s_Mincut_algorithm.svg
    graph = Graph.from_iterable(
        {
            "1": ["2", "3", "4", "5"],
            "2": ["1", "3", "4", "5"],
            "3": ["1", "2", "4", "5", "10"],
            "4": ["1", "2", "3", "5", "6"],
            "5": ["1", "2", "3", "4", "7"],
            "6": ["7", "8", "9", "10", "4"],
            "7": ["6", "8", "9", "10", "5"],
            "8": ["6", "7", "9", "10"],
            "9": ["6", "7", "8", "10"],
            "10": ["6", "7", "8", "9", "3"],
        }
    )

    partitions = kargers(graph)

    assert partitions == {("8", "6"), ("8", "7"), ("8", "10"), ("8", "9")}
