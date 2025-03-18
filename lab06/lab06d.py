# type: ignore

from dataclasses import dataclass
from collections import deque
from math import inf
from collections.abc import Sequence


@dataclass
class Edge:
    i: int
    j: int
    cap: int
    flow: int = 0
    back: "Edge | None" = None

    @property
    def res(self):
        return self.cap - self.flow

    @property
    def is_saturated(self):
        return self.res == 0

    def add_flow(self, f):
        self._add_flow(+f)
        self.back._add_flow(-f)

    def _add_flow(self, f):
        assert self.flow + f <= self.cap
        self.flow += f


class NetworkFlow:
    def __init__(self, n, s, t, r):
        self.n = n
        self.s = s
        self.t = t
        self.r = r
        self.adj = [[] for _ in range(n)]
        super().__init__()

    def add_edge(self, i, j, c):
        edge_ij = Edge(i, j, c)
        edge_ji = Edge(j, i, 0)

        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)

    def find_augmenting_path(self):
        q = deque([self.s])
        pedge = [None] * self.n
        pedge[self.s] = True

        while q:
            i = q.popleft()

            if i == self.t:
                path = []
                while i != self.s:
                    path.append(pedge[i])
                    i = pedge[i].i
                return path

            for edge in self.adj[i]:
                if not edge.is_saturated and pedge[edge.j] is None:
                    pedge[edge.j] = edge
                    q.append(edge.j)

        return None

    def augment(self, path):
        min_flow = min(edge.res for edge in path)
        assert min_flow > 0
        for edge in path:
            edge.add_flow(min_flow)
        return min_flow

    def max_flow(self):
        mf = 0
        path = self.find_augmenting_path()
        # all paths have fixed length (s->r->s->t)
        coords = []
        while path is not None:
            mf += self.augment(path)
            # coords.append((path[1].i, path[1].j))
            path = self.find_augmenting_path()

        for i in range(self.r):
            for edge in self.adj[i]:
                if edge.flow > 0 and edge.j >= self.r:
                    coords.append((i, edge.j))

        return mf, coords

    def netflow(self, i):
        return sum(edge.flow for edge in self.adj[i])


def dispatch(r: Sequence[int], c: Sequence[int]) -> str | None:

    grid = ["."*len(c)]*len(r)

    s = len(r) + len(c)
    t = s+1

    nf = NetworkFlow(t+1, s, t, len(r))

    for i in range(len(r)):
        nf.add_edge(s, i, r[i])

    for i in range(len(c)):
        nf.add_edge(len(r)+i, t, c[i])

    for i in range(len(r)):
        for j in range(len(c)):
            nf.add_edge(i, len(r)+j, 1)

    mf, coords = nf.max_flow()

    if mf != sum(r) or mf != sum(c):
        return None

    for i, j in coords:
        row = ""
        for ch in range(len(c)):
            if ch == j-len(r):
                row += "J"
                continue
            row += grid[i][ch]

        grid[i] = row

    ans = ""
    for row in grid:
        ans += "".join(row) + "\n"

    return ans
