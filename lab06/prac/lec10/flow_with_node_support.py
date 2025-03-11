# type: ignore

from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar, List, Dict, Optional, Set

T = TypeVar("T")  # Generic type for nodes
INFINITY = 10**9  # A large number to simulate infinite capacity

@dataclass
class Edge(Generic[T]):
    """Directed edge from i to j with capacity cap."""
    i: T
    j: T
    cap: int
    flow: int = 0
    back: Optional["Edge[T]"] = None

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
        assert self.flow + f <= self.cap, f"Flow overflow on edge {self.i}->{self.j}"
        self.flow += f


class FlowNetwork(Generic[T]):
    def __init__(self, nodes: Set[T], s: T, t: T, node_caps: Dict[T, int]):
        """
        :param nodes: The set of original nodes.
        :param s: The source node (unsplit form, e.g. "A").
        :param t: The sink node (unsplit form, e.g. "D").
        :param node_caps: A dictionary mapping nodes to their capacities.
        """
        self.orig_s = s
        self.orig_t = t
        self.node_caps = node_caps  # Store node capacities
        self.adj: Dict[str, List[Edge[str]]] = {}

        # Convert nodes into a split-node model
        self._transform_graph(nodes)

        # Define source and sink in the split-node model.
        self.s = f"{s}_in"
        self.t = f"{t}_out"

    def _transform_graph(self, nodes: Set[T]):
        """Transforms the original nodes into a flow network with node capacities."""
        for v in nodes:
            v_in, v_out = f"{v}_in", f"{v}_out"
            self.adj[v_in] = []
            self.adj[v_out] = []
            # Use provided capacity if available; otherwise, use a large number
            cap = self.node_caps[v] if v in self.node_caps else INFINITY
            self.add_edge(v_in, v_out, cap)

    def add_edge(self, i: str, j: str, cap: int):
        """Adds an edge between two nodes."""
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)  # Reverse edge for the residual graph

        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)

        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

    def connect_with_node_caps(self, i: T, j: T, cap: int):
        """Connects two original nodes while respecting node splitting."""
        i_out, j_in = f"{i}_out", f"{j}_in"
        self.add_edge(i_out, j_in, cap)

    def find_augmenting_path(self):
        """Finds an augmenting path using BFS."""
        que = deque([self.s])
        pedge = {node: None for node in self.adj}
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
        """Augments flow along the given path."""
        delta = min(edge.res for edge in path)
        assert delta > 0
        for edge in path:
            edge.add_flow(delta)
        return delta

    def max_flow(self) -> int:
        """Computes the maximum flow in the network."""
        max_flow_value = 0
        while (path := self.find_augmenting_path()) is not None:
            max_flow_value += self.augment(path)
        return max_flow_value

    def min_cut(self):
        """
        Computes the min cut of the network after max flow has been calculated.
        Returns a tuple:
          - A set of nodes (in the split model) reachable from the source in the residual graph.
          - A list of edges crossing from reachable nodes to non-reachable nodes.
        """
        # Find all nodes reachable from the source in the residual network.
        reachable = set()
        queue = deque([self.s])
        reachable.add(self.s)
        while queue:
            u = queue.popleft()
            for edge in self.adj[u]:
                if edge.res > 0 and edge.j not in reachable:
                    reachable.add(edge.j)
                    queue.append(edge.j)

        # The min cut edges are those from a reachable node to a non-reachable node.
        cut_edges = []
        for u in reachable:
            for edge in self.adj[u]:
                if edge.j not in reachable and edge.cap > 0:
                    cut_edges.append(edge)
        return reachable, cut_edges

def min_cut_original_nodes(network: FlowNetwork, original_nodes: set[str]) -> list[str]:
    reachable, _ = network.min_cut()
    # For each original node, check if its "in" node is reachable but its "out" node is not.
    return [v for v in original_nodes if f"{v}_in" in reachable and f"{v}_out" not in reachable]

def min_cut_original_edges(network: FlowNetwork, original_nodes: set[str]):
    """
    Returns a list of original graph cut edges.
    Each edge is represented as a tuple (u, v, capacity, flow), where u and v are original node names.
    """
    # Get the cut edges from the residual graph (in split-node format)
    _, cut_edges = network.min_cut()
    original_cut_edges = []
    for edge in cut_edges:
        # Check if the edge is an original edge (from a node's _out to another's _in)
        if edge.i.endswith("_out") and edge.j.endswith("_in"):
            # Strip the '_out' and '_in' suffixes to recover the original node names
            u = edge.i[:-4]  # remove '_out'
            v = edge.j[:-3]  # remove '_in'
            original_cut_edges.append((u, v, edge.cap, edge.flow))
    return original_cut_edges


if __name__ == "__main__":
    nodes = {"A", "B", "C", "D"}
    source, sink = "A", "D"  # Use unsplit node names here

    # Define node capacities for internal nodes; source and sink default to high capacity.
    node_caps = {"B": 3, "C": 4}

    # Initialize the network
    network = FlowNetwork(nodes, source, sink, node_caps)

    # Connect nodes with edges (the code handles node splitting automatically)
    network.connect_with_node_caps("A", "B", 5)
    network.connect_with_node_caps("B", "C", 3)
    network.connect_with_node_caps("C", "D", 4)

    print(network.max_flow())  # Compute and print the maximum flow

    # Compute the min cut (reachable nodes and the cut edges)
    reachable, cut_edges = network.min_cut()
    print("Reachable nodes in residual graph (min cut source side):", reachable)
    print("Min cut edges:")
    for edge in cut_edges:
        print(f"{edge.i} -> {edge.j} (capacity: {edge.cap}, flow: {edge.flow})")

    cut_nodes_og = min_cut_original_nodes(network, nodes)
    print("Cut nodes", cut_nodes_og)

    cut_edges_og = min_cut_original_edges(network, nodes)
    print("Cut edges", cut_edges_og)
