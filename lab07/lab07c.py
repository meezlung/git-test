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
    

def max_caught(city: str) -> int:
    lines = city.splitlines()
    if not lines:
        return 0
    
    r = len(lines)
    c = len(lines[0])

    grid = [list(line) for line in lines]

    # assign an id to each non-building cell
    cell_to_id = {}
    id_counter = 0
    for i in range(r):
        for j in range(c):
            if grid[i][j] != "#":
                cell_to_id[(i, j)] = id_counter
                id_counter += 1

    N = id_counter
    # total nodes = 2 * N (for in and out) + 2 (for source and sink)
    source = 2 * N
    sink = 2 * N + 1
    
    n = 2 * N + 2
    
    fn = FlowNetwork(n, source, sink)

    
    # for each non-building cell, add an edge from its "in" node to "out" node (cap = 1)
    for (i, j), node in cell_to_id.items():
        fn.add_edge(node, node + N, 1)

    # add edges for valid movements (orthogonal neighbors)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for (i, j), node in cell_to_id.items():
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if (ni, nj) in cell_to_id:
                neighbor = cell_to_id[(ni, nj)]
                fn.add_edge(node + N, neighbor, 1)

    # connect the mega source to allies and culprits to the mega sink
    for (i, j), node in cell_to_id.items():
        if grid[i][j] == 'L':
            fn.add_edge(source, node, 1)
        if grid[i][j] == 'C':
            fn.add_edge(node + N, sink, 1)


    return fn.max_flow()
    
print(max_caught("""\
L..L
..C.
.L..
C..C
"""))

print(max_caught("""\
LLL.C
L.#.C
....C
"""))