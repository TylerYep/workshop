import random
from collections import defaultdict
from typing import Any, Dict, List, Set

Vertex = int
INFINITY = 10000


class UIntPQueue:
    """
    A priority queue that does not allow repeats. When a repeat value is
    enqueued, it is updated with the smaller priority. The queue only allows
    nonnegative integers up to a max value.
    """

    def __init__(self) -> None:
        from src.structures import FibonacciHeap

        self.fheap = FibonacciHeap[Vertex]()
        self.entries: Dict[Vertex, int] = {}

    def __len__(self) -> int:
        return len(self.fheap)

    def enqueue(self, value: Vertex, priority: float) -> None:
        if value not in self.entries:
            self.fheap.enqueue(value, priority)
        elif priority < self.entries[value]:
            self.fheap.decrease_key(value, priority)

    def dequeue_min(self) -> Any:
        value, _ = self.fheap.dequeue_min()
        # del self.entries[value]
        return value


class ApproxDistanceOracle:
    def __init__(self, V: Set[Vertex], E: List[List[Vertex]], k: int = 2) -> None:
        """
        Preprocessing step.
        Note that:
            self.p represents witnesses
            self.a_i_v_distances represents delta(A_i, v)
        """
        self.E = E
        self.n = len(V)  # number of vertices

        # Create lists of neighbors
        self.neighbors: List[List[Vertex]] = [[] for _ in V]
        for u in V:
            for v in range(u):
                if E[u][v] != INFINITY:
                    self.neighbors[u].append(v)
                    self.neighbors[v].append(u)

        # Initialize k+1 sets of vertices with decreasing sizes. (i-centers)
        self.A: List[Set[Vertex]] = [V] * (k + 1)
        self.A[0] = V
        self.A[k] = set()
        for i in range(1, k):  # for i = 1 to k - 1
            prob = self.n ** (-1 / k)
            self.A[i] = {x for x in self.A[i - 1] if weighted_coin_flip(prob)}

        self.a_i_v_distances: List[List[float]] = [
            [None] * self.n for _ in range(k + 1)  # type: ignore[list-item]
        ]
        self.p: List[List[Vertex]] = [
            [None] * self.n for _ in range(k + 1)  # type: ignore[list-item]
        ]

        # Initialize a_i_v_distances of A_k to INFINITY
        self.a_i_v_distances[k] = [INFINITY] * self.n
        self.p[k] = [None] * self.n  # type: ignore[list-item]

        # Initialize empty bunches
        self.B: List[Set[Vertex]] = [{v} for v in V]

        # Initialize table of calculated distances
        self.distances = defaultdict(lambda: INFINITY)
        for v in V:
            self.distances[(v, v)] = 0

        for i in range(k - 1, -1, -1):  # for i = k - 1 down to 0
            # compute delta(A_i, v) for each v in V
            self.compute_delta_a_i_v(i)

            # compute distances and bunches
            self.compute_vertex_distances(i)

    def query(self, u: Vertex, v: Vertex) -> float:
        w = u
        i = 0
        while w not in self.B[v]:
            i += 1
            u, v = v, u
            w = self.p[i][u]
        return self.distances[(w, u)] + self.distances[(w, v)]

    def compute_delta_a_i_v(self, i: int) -> None:
        """ Variant on Dijkstra's that tracks witnesses. """
        q = UIntPQueue()
        self.a_i_v_distances[i] = [INFINITY] * self.n
        self.p[i] = [INFINITY] * self.n
        for w in self.A[i]:
            self.a_i_v_distances[i][w] = 0
            self.p[i][w] = w
            # Instead of adding and later removing a new source vertex, just
            # enqueue everything in A_i
            q.enqueue(w, 0)
        while len(q) > 0:
            w = q.dequeue_min()
            for v in self.neighbors[w]:
                prev = self.a_i_v_distances[i][v]
                nxt = self.a_i_v_distances[i][w] + self.E[w][v]
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
            while len(q) > 0:
                w = q.dequeue_min()
                for v in self.neighbors[w]:
                    nxt = self.distances[(c, w)] + self.E[w][v]
                    # Only store the distance if the i-center c is closer to v
                    # than everything in A_(i+1)
                    if nxt < self.a_i_v_distances[i + 1][v]:
                        prev = self.distances[(c, v)]
                        if nxt < prev:
                            self.distances[(c, v)] = nxt
                            self.B[v].add(c)
                            q.enqueue(v, nxt)


def weighted_coin_flip(prob: float) -> bool:
    """ Returns True with probability prob. """
    return random.choices([True, False], [prob, 1 - prob])[0]
