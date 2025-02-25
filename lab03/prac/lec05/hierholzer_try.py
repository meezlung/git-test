from dataclasses import dataclass

@dataclass
class Edge:
    i: str
    j: str
    cost: int | None = None
    
    def reverse(self):
        return Edge(self.j, self.i, self.cost)

@dataclass
class Adj:
    j: str
    cost: int | None = None
    edge: Edge | None = None
    idx: int = -1

    def iter(self):
        yield self.j
        yield self.cost
        yield self.edge
        yield self.idx

def is_connected(n: int, edges: list[Edge], adj_list: dict[str, list[Adj]]):
    if not edges: 
        return False
    
    visited: set[str] = set()

    def dfs(node: str):
        stack = [node]

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for neighbor in adj_list[current]:
                    stack.append(neighbor.j)

    start_node = next(iter(adj_list))
    dfs(start_node)

    return len(visited) == len(adj_list)

def make_adj_list(n: int, edges: list[Edge]):
    adj_list: dict[str, list[Adj]] = {edge.i: [] for edge in edges}

    for edge in edges:
        adj_list[edge.j] = []

    for edge_idx, edge in enumerate(edges):
        adj_list[edge.i].append(Adj(j=edge.j, cost=edge.cost, edge=edge, idx=edge_idx))
        adj_list[edge.j].append(Adj(j=edge.i, cost=edge.cost, edge=edge, idx=edge_idx))

    return adj_list

def _find_eulerian_path(n: int, edges: list[Edge], s: str, t: str):
    adj = make_adj_list(n, edges)

    used_edges = [False]*len(edges)
    rem_path: list[Adj] = []

    def consume_path(i: str, t: str):
        # consume a path from i, then expect to finish at t
        # "just walk arbitrarily"
        path: list[Adj] = []
        while adj[i]:
            a = adj[i].pop()
            if not used_edges[a.idx]:
                used_edges[a.idx] = True
                path.append(a)
                i = a.j # walk once

        while path:
            rem_path.append(path.pop())

        # expect to finish at t here

        # it's not always the case that if u start from i u also end at t
        assert i == t

    # consume path from s to t
    consume_path(s, t)

    # remaining components here now are CC's with even degrees
    eul_path: list[Adj] = [Adj(s)]
    while rem_path:
        i = eul_path[-1].j

        # consume an actual eulerian path on the component containing i
        consume_path(i, i)

        eul_path.append(rem_path.pop())

    return eul_path

def find_eulerian_path(n: int, edges: list[Edge]):
    # assume the graph is connected here
    adj_list = make_adj_list(n, edges)
    if not is_connected(n, edges, adj_list):
        return None

    # compute nodes
    nodes: set[str] = set()
    for edge in edges:
        nodes.add(edge.i)
        nodes.add(edge.j)
    node_idx: dict[str, int] = {node: idx for idx, node in enumerate(nodes)}

    print(node_idx)

    # compute degrees of each node
    deg = [0]*n
    for edge in edges:
        deg[node_idx[edge.i]] += 1
        deg[node_idx[edge.j]] += 1

    odd_nodes = [i for i in range(n) if deg[i] % 2 != 0]

    assert len(odd_nodes) % 2 == 0

    if len(odd_nodes) == 2:
        s, t = [node for node, idx in node_idx.items() if idx in odd_nodes] # start at nodes with odd degree
        print(s, t)
        return _find_eulerian_path(n, edges, s, t)
    elif len(odd_nodes) == 0:
        s, t = next(iter(nodes)), next(iter(nodes))
        print(s, t)
        return _find_eulerian_path(n, edges, s, t)
    

ans = find_eulerian_path(5, [
    Edge("A", "B"),
    Edge("B", "C"),
    Edge("C", "D"),
    Edge("D", "A"),
    Edge("E", "A"),
    Edge("E", "D"),
])

if ans is not None:
    for i in ans:
        print(i)   
else:
    print("No Euler path")


ans = find_eulerian_path(5, [
    Edge("A", "B"),
    Edge("C", "D"),
])

if ans is not None:
    for i in ans:
        print(i)
else:
    print("No Euler path")
