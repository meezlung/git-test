from dataclasses import dataclass

@dataclass
class Edge:
    i: str
    j: str
    cost: int | None = None

@dataclass
class Adj:
    j: str
    cost: int | None = None
    edge: Edge | None = None
    idx: int = -1

def is_connected(adj: dict[str, list[Adj]]):
    visited: set[str] = set()

    def dfs(node: str):
        stack: list[str] = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for neighbor in adj[current]:
                    stack.append(neighbor.j)

    start_node = next(iter(adj))
    dfs(start_node)

    return len(visited) == len(adj)

def make_adj_list(n: int, edges: list[Edge]):
    adj_list: dict[str, list[Adj]] = {edge.i: [] for edge in edges}

    for edge in edges:
        adj_list[edge.j] = []

    for edge_idx, edge in enumerate(edges):
        adj_list[edge.i].append(Adj(edge.j, edge.cost, edge, edge_idx))
        adj_list[edge.j].append(Adj(edge.i, edge.cost, edge, edge_idx))

    return adj_list

def _find_eulerian_path(n: int, edges: list[Edge], s: str, t: str):
    adj_list = make_adj_list(n, edges)

    used_edges = [False]*len(edges)
    rem_path: list[Adj] = []

    def consume_path(i: str, t: str):
        # start at i, expect to end at t
        path: list[Adj] = []
        while adj_list[i]:
            a = adj_list[i].pop()
            if not used_edges[a.idx]:
                used_edges[a.idx] = True
                path.append(a)
                i = a.j

        while path:
            rem_path.append(path.pop())

        assert i == t

    consume_path(s, t)

    eul_path: list[Adj] = [Adj(s)]
    while rem_path:
        i = eul_path[-1].j

        consume_path(i, i)

        eul_path.append(rem_path.pop())

    return eul_path

def find_eulerian_path(n: int, edges: list[Edge]):
    # assume graph is connected
    adj = make_adj_list(n, edges)

    if not is_connected(adj):
        return None


    # find deg
    nodes: set[str] = set()
    for edge in edges:
        nodes.add(edge.i)
        nodes.add(edge.j)
    node_idx: dict[str, int] = {node: i for i, node in enumerate(nodes)}

    deg = [0]*n
    for edge in edges:
        deg[node_idx[edge.i]] += 1
        deg[node_idx[edge.j]] += 1

    odd_nodes = [i for i in range(n) if deg[i] % 2 != 0]

    assert len(odd_nodes) % 2 == 0

    if len(odd_nodes) == 2:
        s, t = [node for node, idx in node_idx.items() if idx in odd_nodes]
        return _find_eulerian_path(n, edges, s, t)
    elif len(odd_nodes) == 0:
        s, t = next(iter(nodes)), next(iter(nodes))
        return _find_eulerian_path(n, edges, s, t)
    
    return None


ans = find_eulerian_path(5, [
    Edge("A", "B"),
    Edge("B", "C"),
    Edge("C", "D"),
    Edge("D", "A"),
    # Edge("E", "A"),
    # Edge("E", "D"),
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
