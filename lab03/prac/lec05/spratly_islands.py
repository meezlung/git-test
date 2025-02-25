import sys
from typing import Union, List, Dict

class Edge:
    def __init__(self, i: int, j: int, cost: Union[int, None] = None):
        self.i = i
        self.j = j
        self.cost = cost

class Adj:
    def __init__(self, j: int, cost: Union[int, None] = None, edge: Union[Edge, None] = None, idx: int = -1):
        self.j = j
        self.cost = cost
        self.edge = edge
        self.idx = idx

    def iter(self):
        yield self.j
        yield self.cost
        yield self.edge
        yield self.idx

def make_adj_List(n: int, edges: List[Edge]):
    adj_List: Dict[int, List[Adj]] = {i: [] for i in range(n + 1)}

    for edge_idx, edge in enumerate(edges):
        adj_List[edge.i].append(Adj(edge.j, edge.cost, edge, edge_idx))
        adj_List[edge.j].append(Adj(edge.i, edge.cost, edge, edge_idx))

    return adj_List

def _find_eulerian_path(n: int, edges: List[Edge], s: int, t: int):
    adj_List = make_adj_List(n, edges)

    used_edges = [False]*len(edges)
    rem_path: List[Adj] = []

    def consume_path(i: int, t: int):
        path: List[Adj] = []
        while adj_List[i]:
            a = adj_List[i].pop()
            if not used_edges[a.idx]:
                used_edges[a.idx] = True
                path.append(a)
                i = a.j

        while path:
            rem_path.append(path.pop())

        assert i == t

    consume_path(s, t)

    eul_path: List[Adj] = [Adj(s)]
    while rem_path:
        i = eul_path[-1].j

        consume_path(i, i)

        eul_path.append(rem_path.pop())

    return eul_path

def find_eulerian_path(n: int, edges: List[Edge]):
    # assume connected graph

    # compute deg
    deg = [0]*(n + 1)
    for edge in edges:
        deg[edge.i] += 1
        deg[edge.j] += 1

    odd_edges = [i for i in range(n + 1) if deg[i] % 2 != 0]

    assert len(odd_edges) % 2 == 0

    if len(odd_edges) <= 2:
        return _find_eulerian_path(n, edges, *(odd_edges[:2] or (1, 1)))
    
    return None


T = int(sys.stdin.readline())

for t in range(T):
    N = int(sys.stdin.readline().strip())

    nodes: List[int] = [i for i in range(1, N + 1)] # 1-indexed

    # get N - 2 north and south bridges
    north_bridges = list(map(int, sys.stdin.readline().split()))
    south_bridges = list(map(int, sys.stdin.readline().split()))

    # there will be 2(N - 2) bridges in total

    # make List of edges
    edges: List[Edge] = []
    
    # process north
    for i in range(1, N - 1):
        edges.append(Edge(nodes[i], north_bridges[i - 1]))
        edges.append(Edge(nodes[i], south_bridges[i - 1]))

    ans = find_eulerian_path(N, edges)

    if ans is None:
        print("NO")
    else:
        print("YES")
        print(2*(N - 2) - 1)
        print(" ".join([str(a.j) for idx, a in enumerate(ans) if idx != 0]))