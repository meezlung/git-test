from dataclasses import dataclass

@dataclass
class Edge:
    i: int
    j: int
    cost: int | None = None


@dataclass
class Adj:
    j: int
    cost: int | None = None
    edge: "Edge | None" = None
    idx: int = -1

def is_connected(adj_list: dict[int, list[Adj]]):
    visited: set[int] = set()

    def dfs(node: int):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for neighbor in adj_list[current]:
                    stack.append(neighbor.j)

    start_node = next(iter(adj_list))
    dfs(start_node)

    return len(adj_list) == len(visited)

def make_adj_list(n: int, edges: list[Edge]):
    adj_list: dict[int, list[Adj]] = {i: [] for i in range(n)}

    for edge_idx, edge in enumerate(edges):
        adj_list[edge.i].append(Adj(j=edge.j, cost=edge.cost, edge=edge, idx=edge_idx))
        adj_list[edge.j].append(Adj(j=edge.i, cost=edge.cost, edge=edge, idx=edge_idx))

    return adj_list

def _find_eulerian_path(n: int, edges: list[Edge], s: int, t: int):
    adj_list = make_adj_list(n, edges)

    used_edges = [False]*len(edges)
    rem_path: list[Adj] = []

    def consume_path(i: int, t: int):
        # start at i, then expect to finish at t
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
        # node walked by walk once        
        i = eul_path[-1].j

        # just walk and consume eulerian cycle to the path containing i
        consume_path(i, i)

        eul_path.append(rem_path.pop())
    
    return eul_path


def find_eulerian_path(n: int, edges: list[Edge]):
    # assume graph is connected here
    adj = make_adj_list(n, edges)

    if not is_connected(adj):
        return None
    
    # compute deg
    deg = [0]*n
    for edge in edges:
        deg[edge.i] += 1
        deg[edge.j] += 1

    odd_nodes = [i for i in range(n) if deg[i] % 2 != 0]

    assert len(odd_nodes) % 2 == 0

    if len(odd_nodes) == 2:
        s, t = odd_nodes[:2]
        return _find_eulerian_path(n, edges, s, t)
    elif len(odd_nodes) == 0:
        s, t = (0, 0)
        return _find_eulerian_path(n, edges, s, t)

    return None


ans = (find_eulerian_path(5, [
    Edge(0, 1),
    Edge(1, 2),
    Edge(2, 3),
    Edge(3, 4),
    Edge(1, 4),
    Edge(1, 3),
]))

if ans:
    for a in ans:
        print(a.j)