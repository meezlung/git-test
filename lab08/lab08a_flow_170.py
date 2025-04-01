# type: ignore

from collections import deque
from dataclasses import dataclass

@dataclass
class Edge:
    """directed edge from i to j with capacity cap"""
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

# Edmonds-Karp max flow implementation
class FlowNetwork:
    def __init__(self, n, s, t):
        self.n = n
        self.s = s
        self.t = t
        self.adj = [[] for _ in range(n)]
        super().__init__()

    def add_edge(self, i, j, cap):
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)
        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)
        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

    def find_augmenting_path(self):
        que = [self.s]
        pedge = [None] * self.n
        pedge[self.s] = True

        while que:
            i = que.pop()
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
        assert delta > 0
        for edge in path:
            edge.add_flow(delta)
        return delta

    def max_flow(self):
        max_flow_value = 0
        while (path := self.find_augmenting_path()) is not None:
            max_flow_value += self.augment(path)
        return max_flow_value

    def netflow(self, i):
        return sum(edge.flow for edge in self.adj[i])


def choose_faces(dice):
    d = len(dice)
    # Compute the overall maximum face value among all dice.
    max_all = max(face for die in dice for face in die)
    
    # We'll try candidate starting values C from 1 up to max_all - d + 1.
    for C in range(1, max_all - d + 2):
        # Build the flow network.
        # Nodes:
        #   0: source
        #   1 .. d: dice nodes
        #   d+1 .. 2d: position nodes (position p corresponds to number C+p)
        #   2d+1: sink
        n = 2 * d + 2
        source = 0
        sink = 2 * d + 1
        network = FlowNetwork(n, source, sink)

        # We'll store mapping from (die_node, pos_node) to the face index (1-indexed)
        mapping = {}

        # Source -> dice nodes.
        for i in range(d):
            network.add_edge(source, 1 + i, 1)

        # Position nodes -> sink.
        for p in range(d):
            network.add_edge(1 + d + p, sink, 1)

        # For each die (node 1+i) add an edge to position node (d+1+p)
        # if the die has a face equal to C+p.
        for i, die in enumerate(dice):
            for face_index, face_val in enumerate(die, start=1):
                p = face_val - C
                if 0 <= p < d:
                    die_node = 1 + i
                    pos_node = 1 + d + p
                    if (die_node, pos_node) not in mapping:
                        mapping[(die_node, pos_node)] = face_index
                        network.add_edge(die_node, pos_node, 1)

        # Compute the maximum flow. If it equals d, we have a perfect matching.
        if network.max_flow() == d:
            result = [None] * d
            for i in range(d):
                die_node = 1 + i
                for edge in network.adj[die_node]:
                    # Check if this edge goes to a position node and carries flow.
                    if (d + 1) <= edge.j <= (2 * d) and edge.flow == 1:
                        result[i] = mapping[(die_node, edge.j)]
                        break
            if None not in result:
                return result

    # Given the problem guarantee, we should never reach here.
    return []