# type: ignore 

from collections import deque
from dataclasses import dataclass
import sys

# FlowNetwork code (Edmonds–Karp)
INF = 10**9

@dataclass
class Edge:
    """Directed edge from i to j with capacity cap."""
    i: int
    j: int
    cap: int
    flow: int = 0
    back: "Edge | None" = None

    @property
    def is_saturated(self):
        return self.cap - self.flow == 0

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
        self.adj = [[] for _ in range(n)]

    def add_edge(self, i, j, cap):
        # Create edge and reverse edge.
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)
        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)
        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

    def find_augmenting_path(self):
        que = deque([self.s])
        pedge = [None] * self.n
        pedge[self.s] = True  # mark source as visited

        while que:
            i = que.popleft()
            if i == self.t:
                # Reconstruct path from s to t.
                path = []
                while i != self.s:
                    path.append(pedge[i])
                    i = pedge[i].i
                return path[::-1]  # reverse path to get correct order

            for edge in self.adj[i]:
                if not edge.is_saturated and pedge[edge.j] is None:
                    pedge[edge.j] = edge
                    que.append(edge.j)
        return None

    def augment(self, path):
        delta = min(edge.res for edge in path)
        assert delta > 0
        for edge in path:
            edge.add_flow(delta)
        return delta

    def max_flow(self):
        max_flow_value = 0
        while (path := self.find_augmenting_path()) is not None:
            max_flow_value += self.augment(path)
        return max_flow_value

# Main solution using the bipartite graph model.
def main():
    input_data = sys.stdin.read().split()
    H = int(input_data[0])
    W = int(input_data[1])
    grid = [input_data[2+i] for i in range(H)]
    
    # Define node indices.
    # source = 0, sink = 1
    # rows: nodes 2 to 2+H-1  (node for row i is 2+i)
    # columns: nodes 2+H to 2+H+W-1 (node for column j is 2+H+j)
    n_nodes = 2 + H + W
    fn = FlowNetwork(n_nodes, 0, 1)

    S_r, S_c = -1, -1
    T_r, T_c = -1, -1
    for i in range(H):
        for j in range(W):
            ch = grid[i][j]
            if ch == 'S':
                S_r, S_c = i, j
            elif ch == 'T':
                T_r, T_c = i, j

    # For every cell with a leaf ('o', 'S', or 'T'), add an edge between the corresponding row and column.
    # (This edge represents the leaf and is removable with cost 1 unless it is S or T.)
    for i in range(H):
        for j in range(W):
            ch = grid[i][j]
            if ch == '.':
                continue
            row_node = 2 + i
            col_node = 2 + H + j
            if ch == 'S' or ch == 'T':
                cap = INF  # cannot remove S or T
            else:
                cap = 1
            # Add edges in both directions (simulate an undirected edge).
            fn.add_edge(row_node, col_node, cap)
            fn.add_edge(col_node, row_node, cap)

    # Connect source to S’s row and column.
    if S_r != -1 and S_c != -1:
        fn.add_edge(0, 2 + S_r, INF)
        fn.add_edge(0, 2 + H + S_c, INF)

    # Connect T’s row and column to sink.
    if T_r != -1 and T_c != -1:
        fn.add_edge(2 + T_r, 1, INF)
        fn.add_edge(2 + H + T_c, 1, INF)

    flow = fn.max_flow()
    if flow >= INF:
        print(-1)
    else:
        print(flow)

if __name__ == '__main__':
    main()
