# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass
from collections import deque
from math import inf

@dataclass
class Edge:
    i: str
    j: str
    cap: int
    flow: int = 0
    back: "Edge | None" = None

    @property
    def is_saturated(self) -> bool:
        return self.res == 0

    @property
    def res(self) -> int:
        return self.cap - self.flow

    def add_flow(self, f: int):
        self._add_flow(+f)
        if self.back:
            self.back._add_flow(-f)

    def _add_flow(self, f: int):
        # assert self.flow + f <= self.cap
        self.flow += f

class FlowNetwork:
    def __init__(self, nodes: list[int], s: int, t: int, node_caps: dict[int, int]):
        self.orig_s = s
        self.orig_t = t
        self.node_caps = node_caps  # store node capacities
        self.adj: dict[int, list[Edge[int]]] = {}

        # convert nodes into a split-node model
        self._transform_graph(nodes)

        # define source and sink in the split-node model.
        self.s = f"{s}_in"
        self.t = f"{t}_out"

    def _transform_graph(self, nodes: list[int]):
        for v in nodes:
            v_in, v_out = f"{v}_in", f"{v}_out"
            self.adj[v_in] = []
            self.adj[v_out] = []
            cap = self.node_caps[v] if v in self.node_caps else inf
            self.add_edge(v_in, v_out, cap)

    def add_edge(self, i: int, j: int, cap: int):
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)  

        if i not in self.adj:
            self.adj[i] = []
        self.adj[i].append(edge_ij)

        if j not in self.adj:
            self.adj[j] = []
        self.adj[j].append(edge_ji)

        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

        return edge_ij

    def connect_with_node_caps(self, i: int, j: int, cap: int):
        i_out, j_in = f"{i}_out", f"{j}_in"
        return self.add_edge(i_out, j_in, cap)

    def find_augmenting_path(self):
        que = deque([self.s])
        pedge = {}
        pedge[self.s] = None

        while que:
            i = que.popleft()
            if i == self.t:
                path = []
                while i != self.s:
                    path.append(pedge[i])
                    i = pedge[i].i
                return path

            for edge in self.adj.get(i, []):
                if edge.res > 0 and edge.j not in pedge:
                    pedge[edge.j] = edge
                    que.append(edge.j)

        return None

    def augment(self, path):
        delta = min(edge.res for edge in path)
        for edge in path:
            edge.add_flow(delta)
        return delta

    def max_flow(self) -> int:
        max_flow_value = 0
        while (path := self.find_augmenting_path()) is not None:
            max_flow_value += self.augment(path)
        return max_flow_value

def packet_flood(
        computer_limits: Sequence[int],
        connections: Sequence[tuple[int, int, int]],
    ) -> tuple[int, list[int], list[int]]:

    n = len(computer_limits)
    nodes = [i for i in range(1, n + 1)]
    node_caps = {i + 1: computer_limits[i] for i in range(n)}

    source = 1
    sink = n

    fn = FlowNetwork(nodes, source, sink, node_caps)
    connection_edges = []

    for u, v, p in connections:
        edge = fn.connect_with_node_caps(u, v, p)
        connection_edges.append(edge)

    max_flow = fn.max_flow()

    nodes_flows = []
    edges_flows = [edge.flow for edge in connection_edges]

    for v in range(1, n + 1):
        v_in = f"{v}_in"
        v_out = f"{v}_out"
        node_flow = 0
        for edge in fn.adj.get(v_in, []):
            if edge.j == v_out:
                node_flow = edge.flow
                break
        nodes_flows.append(node_flow)

    return (
        max_flow,
        edges_flows,
        nodes_flows,
    )

# print(
#     packet_flood([10**12, 4, 10**12], [
#         (1, 2, 5),
#         (2, 3, 5),
#         (1, 3, 7),
#     ])
# )

# print(
#     packet_flood([5, 6], [
#         (1, 2, 7),
#         (1, 2, 7),
#     ])
# )


# print(
#     packet_flood([1, 1], [
#         (1, 2, 1),
#         (1, 2, 1),
#     ])
# )