# type: ignore

from collections import deque
from dataclasses import dataclass
import sys

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
        self._add_flow(f)
        self.back._add_flow(-f)

    def _add_flow(self, f):
        assert self.flow + f <= self.cap, f"Flow {self.flow} + {f} > {self.cap}"
        self.flow += f

class FlowNetwork:
    def __init__(self, n, s, t):
        self.n = n        
        self.s = s        
        self.t = t        
        self.adj = [[] for _ in range(n)]

    def add_edge(self, i, j, cap):
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)
        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)
        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

    def find_augmenting_path(self):
        que = deque([self.s])
        pedge = [None] * self.n  
        pedge[self.s] = True 
        while que:
            i = que.popleft()
            if i == self.t:
                # Reconstruct the path by backtracking.
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

if __name__ == '__main__':
    H, W, N = map(int, sys.stdin.readline().split())

    pieces = []
    for _ in range(N):
        A, B, C, D = map(int, sys.stdin.readline().split())
        pieces.append((A, B, C, D))

    source = 0
    row_start = 1
    piece_in_start = row_start + H
    piece_out_start = piece_in_start + N
    col_start = piece_out_start + N
    sink = col_start + W
    total_nodes = sink + 1

    net = FlowNetwork(total_nodes, source, sink)

    for r in range(1, H + 1):
        net.add_edge(source, r, 1)
    
    for i, (A, B, C, D) in enumerate(pieces):
        piece_node = piece_in_start + i
        for r in range(A, C + 1):
            net.add_edge(r, piece_node, 1)

    # internal edge between piece nodes
    for i in range(N):
        piece_in_node = piece_in_start + i
        piece_out_node = piece_out_start + i
        net.add_edge(piece_in_node, piece_out_node, 1)

    for i, (A, B, C, D) in enumerate(pieces):
        piece_node = piece_out_start + i
        for c in range(B, D + 1):
            col_node = col_start + (c - 1)
            net.add_edge(piece_node, col_node, 1)

    for c in range(1, W + 1):
        col_node = col_start + (c - 1)
        net.add_edge(col_node, sink, 1)

    result = net.max_flow()
    print(result)