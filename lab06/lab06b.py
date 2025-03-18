# type: ignore

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
    def __init__(self, n, s, t):
        self.n = n
        self.s = s
        self.t = t
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
        for edge in path:
            edge.add_flow(min_flow)
        return min_flow

    def bfs_residual(self):
        q = deque([self.s])
        reachable = [False] * self.n
        reachable[self.s] = True

        while q:
            i = q.popleft()

            # check node_out
            for edge in self.adj[i]:
                if not reachable[edge.j] and not edge.is_saturated:
                    reachable[edge.j] = True
                    q.append(edge.j)

        return reachable

    def max_flow(self):
        mf = 0
        path = self.find_augmenting_path()
        while path is not None:
            mf += self.augment(path)
            path = self.find_augmenting_path()

        reachable = self.bfs_residual()

        coords = []

        for i in range(1, self.n, 2):
            if not reachable[i] and reachable[i-1] and i != self.n - 1:
                coords.append(i-1)

        return mf, coords

    def netflow(self, i):
        return sum(edge.flow for edge in self.adj[i])


def place_traps(alleyways: str) -> str:
    grid = alleyways.splitlines()

    r = len(grid)
    c = len(grid[0])

    s = r*c*2
    t = s+1

    nf = NetworkFlow(r*c*2 + 2, s, t)

    def compute_node_id(i, j):
        return i*c + j

    def check_next(i, j, ch, id):
        if not (0 <= i < r and 0 <= j < c):
            return
        curr_ch = grid[i][j]

        if curr_ch != "#":
            id2_in = 2*compute_node_id(i, j)
            id2_out = id2_in + 1
            if (ch == "S" or ch == "D") and (curr_ch == "S" or curr_ch == "D"):
                nf.add_edge(id, id2_in, -1)
                nf.add_edge(id2_out, id-1, -1)

            else:
                nf.add_edge(id, id2_in, inf)
                nf.add_edge(id2_out, id-1, inf)

    dirs = [(1, 0), (0, 1)]

    for i in range(r):
        for j in range(c):
            id_in = 2*compute_node_id(i, j)
            id_out = id_in + 1
            ch = grid[i][j]
            if ch != "S" or ch != "D":
                nf.add_edge(id_in, id_out, 1)
            if ch == "S":
                nf.add_edge(s, id_in, inf)
                nf.add_edge(id_in, id_out, inf)
            elif ch == "D":
                nf.add_edge(id_out, t, inf)
                nf.add_edge(id_in, id_out, inf)

            if ch != "#":
                for x, y in dirs:
                    check_next(i+x, j+y, ch, id_out)

    mf, cuts = nf.max_flow()

    if mf == 0:
        return alleyways

    ans = ""
    for cut in cuts:
        i, j = cut // 2 // c, (cut // 2) % c
        row = ""
        for ch in range(c):
            if ch == j:
                row += "X"
                continue
            row += grid[i][ch]

        grid[i] = row

    for row in grid:
        ans += row
        ans += "\n"

    return ans


#
# place_traps("""\
# .#...#.
# ..#....
# .S.....
# .....D.
# ....#..
# .#...#.
# """)
# place_traps("""\
# #.#.#
# .S...
# #.#.#
# ...D.
# #.#.#
# """)
# place_traps("""\
# S
# .
# #
# .
# .
# D
# """)
# place_traps("""\
# S..#..
# .#.#..
# .#..D.
# """)
# place_traps("""\
# S.....
# ......
# ......
# ......
# .....D
# """)
# place_traps("""\
# S..#...D
# """)
# place_traps("""\
# S.D
# """)
# place_traps("""\
# SD
# """)
# place_traps("""\
# S.#...
# .#.#..
# .#.#.D
# """)
