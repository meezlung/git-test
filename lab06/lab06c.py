# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass
from collections import deque
from math import inf

@dataclass
class Edge:
    i: int
    j: int
    cap: int
    flow: int = 0
    back: "Edge | None" = None

    @property
    def is_saturated(self):
        return self.res == 0

    @property
    def res(self):
        return self.cap - self.flow

    def add_flow(self, f):
        self._add_flow(+f)
        self.back._add_flow(-f)

    def _add_flow(self, f):
        assert self.flow + f <= self.cap
        self.flow += f


class FlowNetwork:
    def __init__(self, n, s, t):
        self.n = n
        self.s = s
        self.t = t
        self.adj= [[] for _ in range(n)]
        super().__init__()


    def add_edge(self, i, j, cap):
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)

        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)

        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

    def find_augmenting_path(self):
        que = deque([self.s])
        pedge = [None]*self.n
        pedge[self.s] = True

        while que:
            i = que.popleft()

            if i == self.t:
                path = []
                while i != self.s:
                    path.append(pedge[i])
                    i = pedge[i].i

                return path

            for edge in self.adj[i]:
                if not edge.is_saturated and pedge[edge.j] is None:
                    pedge[edge.j] = edge
                    que.append(edge.j)

        return None


    def augment(self, path):
        delta = min(edge.res for edge in path)

        for edge in path:
            edge.add_flow(delta)

        return delta


    def max_flow(self):
        max_flow_value = 0

        while (path := self.find_augmenting_path()) is not None:
            max_flow_value += self.augment(path)

        return max_flow_value


    def netflow(self, i: int):
        return sum(edge.flow for edge in self.adj[i])
    

def max_plushies(
        num_sisters: Sequence[int],
        roads: Sequence[tuple[int, int]],
        with_store: Sequence[int]
    ) -> int:

    len_sisters = len(num_sisters)
    # len_stores = len(with_store)
    n = len_sisters + 2

    fn = FlowNetwork(n, 0, n - 1) # megasource 0 megasink n - 1

    max_sister = max(num_sisters)

    # add roads
    for i, j in roads:
        fn.add_edge(i, j, 1) # twoway
        fn.add_edge(j, i, 1)

    # link megasource to all source of sisters
    for i in range(len_sisters):
        # for j in range(num_sisters[i]):
        fn.add_edge(0, i + 1, num_sisters[i])
            # fn.add_edge(i + 1, 0, 1)

    # link megasink to all sinks of stores
    for building in with_store:
        fn.add_edge(building, n - 1, inf)
        # fn.add_edge(n - 1, building, 1)


    return fn.max_flow()

# print(max_plushies([2, 0, 0, 0], [
#         (1, 2),
#         (1, 3),
#         (2, 3),
#         (2, 4),
#         (3, 4),
#     ], [4])
# )


    # # add roads
    # for i, j in roads:
    #     fn.add_edge(i, j, 1) # twoway
    #     fn.add_edge(j, i, 1)

    # # link megasource to all source of sisters
    # for i in range(len_sisters):
    #     for j in range(num_sisters[i]):
    #         fn.add_edge(0, i + 1, 1)
    #         # fn.add_edge(i + 1, 0, 1)

    # # link megasink to all sinks of stores
    # for building in with_store:
    #     fn.add_edge(building, n - 1, inf)
    #     # fn.add_edge(n - 1, building, 1)
