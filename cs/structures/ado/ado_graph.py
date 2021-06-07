from collections import defaultdict

from cs.structures.graph import Graph
from cs.structures.heap.fibonacci_heap import FibonacciHeap
from cs.util import weighted_coin_flip


class ApproxDistanceOracle:
    def __init__(self, graph: Graph[int], k: int = 2) -> None:
        """
        Preprocessing step.
        Note that:
            self.p represents witnesses
            self.a_i_v_distances represents delta(A_i, v)
        """
        self.graph = graph
        self.n = len(graph)

        # Initialize k+1 sets of vertices with decreasing sizes. (i-centers)
        self.A: list[set[int]] = [set()] * (k + 1)
        self.A[0] = set(self.graph)
        self.A[k] = set()
        for i in range(1, k):  # for i = 1 to k - 1
            prob = self.n ** (-1 / k)
            self.A[i] = {x for x in self.A[i - 1] if weighted_coin_flip(prob)}

        self.a_i_v_distances: list[list[float]] = [[0] * self.n for _ in range(k + 1)]
        self.p: list[list[int]] = [[0] * self.n for _ in range(k + 1)]

        # Initialize a_i_v_distances of A_k to INFINITY
        self.a_i_v_distances[k] = [Graph.INFINITY] * self.n
        self.p[k] = [0] * self.n

        # Initialize empty bunches
        self.B: list[set[int]] = [{v} for v in self.graph]

        # Initialize table of calculated distances
        self.distances: dict[tuple[int, int], float] = defaultdict(
            lambda: Graph.INFINITY
        )
        for v in self.graph:
            self.distances[(v, v)] = 0

        # for i = k - 1 down to 0
        for i in range(k - 1, -1, -1):
            # compute delta(A_i, v) for each v in V
            self.compute_delta_a_i_v(i)

            # compute distances and bunches
            self.compute_vertex_distances(i)

    def query(self, u: int, v: int) -> float:
        w = u
        i = 0
        while w not in self.B[v]:
            i += 1
            u, v = v, u
            w = self.p[i][u]
        return self.distances[(w, u)] + self.distances[(w, v)]

    def compute_delta_a_i_v(self, i: int) -> None:
        """Variant on Dijkstra's that tracks witnesses."""
        q = UIntPQueue()
        self.a_i_v_distances[i] = [Graph.INFINITY] * self.n
        self.p[i] = [Graph.INFINITY] * self.n  # type: ignore[list-item]
        for w in self.A[i]:
            self.a_i_v_distances[i][w] = 0
            self.p[i][w] = w
            # Instead of adding and later removing a new source vertex, just
            # enqueue everything in A_i
            q.enqueue(w, 0)
        while q:
            w = q.dequeue()
            for v in self.graph[w]:
                prev = self.a_i_v_distances[i][v]
                nxt = self.a_i_v_distances[i][w] + self.graph[w][v].weight
                if nxt < prev:
                    self.a_i_v_distances[i][v] = nxt
                    self.p[i][v] = self.p[i][w]
                    q.enqueue(v, nxt)

    def compute_vertex_distances(self, i: int) -> None:
        """
        A modified version of Dijkstra's algorithm that only updates delta(c, v)
        if the new estimate of delta(c, v) is strictly smaller than delta(A_(i+1), v).
        """
        q = UIntPQueue()

        # Run Dijkstra's algorithm from each i-center
        for c in self.A[i]:
            q.enqueue(c, 0)
            while q:
                w = q.dequeue()
                for v in self.graph[w]:
                    nxt = self.distances[(c, w)] + self.graph[w][v].weight
                    # Only store the distance if the i-center c is closer to v
                    # than everything in A_(i+1)
                    if nxt < self.a_i_v_distances[i + 1][v]:
                        prev = self.distances[(c, v)]
                        if nxt < prev:
                            self.distances[(c, v)] = nxt
                            self.B[v].add(c)
                            q.enqueue(v, nxt)


class UIntPQueue:
    """
    A priority queue that does not allow repeats. When a repeat value is
    enqueued, it is updated with the smaller priority. The queue only allows
    nonnegative integers.
    """

    def __init__(self) -> None:
        self.fheap = FibonacciHeap[int]()

    def __len__(self) -> int:
        return len(self.fheap)

    def enqueue(self, value: int, priority: float) -> None:
        if value not in self.fheap:
            self.fheap.enqueue(value, priority)
        elif priority < self.fheap[value].value:
            self.fheap.decrease_key(value, priority)

    def dequeue(self) -> int:
        value, _ = self.fheap.dequeue()
        return value
