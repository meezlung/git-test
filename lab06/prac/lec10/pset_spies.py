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


# Edmonds-Karp
class FlowNetwork:
    def __init__(self, n, s, t):
        self.n = n
        self.s = s
        self.t = t
        self.adj = [[] for _ in range(n)]
        super().__init__()


    def add_edge(self, i, j, cap):
        # make the Edge object and its reverse
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)

        # add both to the adjacency list
        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)

        # point to each other
        edge_ij.back = edge_ji
        edge_ji.back = edge_ij


    def find_augmenting_path(self):
        # BFS starting from source
        que = deque([self.s])
        pedge = [None]*self.n
        pedge[self.s] = True

        while que:
            i = que.popleft()

            if i == self.t:
                # we've reached the sink
                path = []
                while i != self.s:
                    path.append(pedge[i])
                    i = pedge[i].i

                return path

            for edge in self.adj[i]:
                # only go through non-saturated edges
                if not edge.is_saturated and pedge[edge.j] is None:
                    pedge[edge.j] = edge
                    que.append(edge.j)

        return None


    def augment(self, path):
        # get amount of flow to push along
        delta = min(edge.res for edge in path)
        assert delta > 0

        # push delta along the path
        for edge in path:
            edge.add_flow(delta)

        return delta


    def max_flow(self):
        max_flow_value = 0

        # while there is still an augmenting path
        while (path := self.find_augmenting_path()) is not None:
            # augment along path
            max_flow_value += self.augment(path)

        # return the value of the max flow
        return max_flow_value


    def netflow(self, i):
        return sum(edge.flow for edge in self.adj[i])




def find_shortest_path_time(n, highways):
    """Finds the shortest path time from city 1 to city n using BFS."""
    adj = [[] for _ in range(n)]
    
    for u, v in highways:
        adj[u].append(v)
        adj[v].append(u)

    # BFS to find shortest path from node 0 to node n-1
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    return dist[n-1], dist  # Shortest path time & distances

def build_flow_network(n, highways, shortest_time, dist):
    """Builds the flow network using only edges that belong to shortest paths."""
    flow_network = FlowNetwork(n, 0, n-1)
    
    for u, v in highways:
        # Only add edges if they belong to a shortest path
        if dist[u] + 1 == dist[v] or dist[v] + 1 == dist[u]:
            flow_network.add_edge(u, v, 3)  # Each edge has a capacity of 3

    return flow_network

def max_spies(n, highways):
    """Finds the maximum number of spies that can reach city n simultaneously."""
    shortest_time, dist = find_shortest_path_time(n, highways)
    
    if shortest_time == -1:
        return 0  # No path exists (shouldn't happen due to problem constraints)

    flow_network = build_flow_network(n, highways, shortest_time, dist)
    return flow_network.max_flow()