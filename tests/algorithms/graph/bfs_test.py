from cs.algorithms import breadth_first_search
from cs.structures import Graph


class TestBFS:
    @staticmethod
    def test_bfs() -> None:
        graph_1 = Graph[str](
            {
                "A": ["B", "C"],
                "B": ["A", "D", "E"],
                "C": ["A", "F"],
                "D": ["B"],
                "E": ["B", "F"],
                "F": ["C", "E"],
            }
        )
        graph_2 = Graph[int]({0: [1, 2], 1: [0, 3, 4], 2: [0, 3], 3: [1], 4: [2, 3]})
        graph_3 = Graph[str](
            {
                "A": ["B", "C", "E"],
                "B": ["A", "D", "E"],
                "C": ["A", "F", "G"],
                "D": ["B"],
                "E": ["A", "B", "D"],
                "F": ["C"],
                "G": ["C"],
            }
        )

        assert breadth_first_search(graph_1, "A", "F") == ["A", "C", "F"]
        assert breadth_first_search(graph_2, 0, 4) == [0, 1, 4]
        assert breadth_first_search(graph_3, "G", "D") == ["G", "C", "A", "B", "D"]

    @staticmethod
    def test_no_search_path() -> None:
        graph = Graph[str]({"a": {}, "b": {}, "c": {}})

        assert breadth_first_search(graph, "a", "b") == []
