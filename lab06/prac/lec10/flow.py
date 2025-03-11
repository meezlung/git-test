# type: ignore

from collections import deque
from dataclasses import dataclass
from typing import Generic, TypeVar, List, Set, Dict, Optional

T = TypeVar("T")  # Generic type for nodes

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
        if self.back is not None:
            self.back._add_flow(-f)

    def _add_flow(self, f: int):
        assert self.flow + f <= self.cap, "Flow cannot exceed capacity"
        self.flow += f

class FlowNetwork(Generic[T]):
    def __init__(self, nodes: List[T], s: T, t: T):
        self.nodes: List[T] = nodes  # List of all nodes
        self.s: T = s  # Source node
        self.t: T = t  # Sink node
        self.adj: Dict[T, List[Edge[T]]] = {node: [] for node in nodes}  # Adjacency list

    def add_edge(self, i: T, j: T, cap: int):
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)  # Reverse edge

        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)

        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

    def find_augmenting_path(self) -> Optional[List[Edge[T]]]:
        que = deque([self.s])
        pedge: Dict[T, Optional[Edge[T]]] = {node: None for node in self.nodes}
        pedge[self.s] = True  # Mark source as visited

        while que:
            i = que.popleft()

            if i == self.t:
                path: List[Edge[T]] = []
                while i != self.s:
                    edge = pedge[i]
                    assert edge is not None
                    path.append(edge)
                    i = edge.i  # Move back through the path
                path.reverse()  # Reverse the path to start from the source
                return path

            for edge in self.adj[i]:
                if not edge.is_saturated and pedge[edge.j] is None:
                    pedge[edge.j] = edge
                    que.append(edge.j)

        return None

    def augment(self, path: List[Edge[T]]) -> int:
        delta = min(edge.res for edge in path)
        assert delta > 0

        for edge in path:
            edge.add_flow(delta)

        return delta

    def max_flow(self) -> int:
        max_flow_value = 0
        while (path := self.find_augmenting_path()) is not None:
            max_flow_value += self.augment(path)
        return max_flow_value

    def netflow(self, i: T) -> int:
        return sum(edge.flow for edge in self.adj[i])

    def get_flow_value(self) -> int:
        """Returns the total flow leaving the source, which equals the max flow value."""
        return sum(edge.flow for edge in self.adj[self.s])

    def reachable_nodes(self) -> Set[T]:
        """
        Returns the set of nodes reachable from the source in the residual graph.
        """
        visited: Set[T] = set()
        stack = [self.s]
        visited.add(self.s)
        while stack:
            u = stack.pop()
            for edge in self.adj[u]:
                if edge.res > 0 and edge.j not in visited:
                    visited.add(edge.j)
                    stack.append(edge.j)
        return visited

    def get_min_cut_edges(self) -> List[Edge[T]]:
        """
        Returns a list of edges that form the min cut.
        These are edges from a reachable node to a non-reachable node in the residual graph.
        """
        reachable = self.reachable_nodes()
        cut_edges: List[Edge[T]] = []
        for u in reachable:
            for edge in self.adj[u]:
                if edge.cap > 0 and edge.j not in reachable:
                    cut_edges.append(edge)
        return cut_edges

    def reset_flows(self):
        """
        Resets the flow for every edge in the network to zero.
        """
        for node in self.nodes:
            for edge in self.adj[node]:
                edge.flow = 0

    def print_network(self):
        """
        Prints all original edges (those with positive capacity) and their current flows.
        """
        for node in self.nodes:
            for edge in self.adj[node]:
                if edge.cap > 0:  # Only print original (non-reverse) edges
                    print(f"Edge from {edge.i} to {edge.j}: {edge.flow}/{edge.cap}")

    def print_min_cut(self):
        """
        Prints the edges that form the min cut.
        """
        cut_edges = self.get_min_cut_edges()
        print("Min Cut Edges:")
        for edge in cut_edges:
            print(f"{edge.i} -> {edge.j} (capacity: {edge.cap})")

if __name__ == "__main__":
    nodes = ["Bank", "A", "B", "Harbor"]
    source = "Bank"
    sink = "Harbor"
    network = FlowNetwork(nodes, source, sink)

    network.add_edge("Bank", "A", 1)
    network.add_edge("Bank", "B", 1)
    network.add_edge("A", "B", 1)
    network.add_edge("A", "Harbor", 1)
    network.add_edge("B", "Harbor", 1)

    print("Max Flow:", network.max_flow())
    print("Flow value from source:", network.get_flow_value())
    print("\nNetwork state:")
    network.print_network()

    print("\nMin cut details:")
    network.print_min_cut()

    # if given lang edges
    # edges = [(1, 2), (2, 3), (3, 4), (1, 3)]  # Example list of edges

    # # Extract unique nodes using a set
    # nodes = set()
    # for i, j in edges:
    #     nodes.add(i)
    #     nodes.add(j)

    # print(nodes)  # Output: {1, 2, 3, 4}
