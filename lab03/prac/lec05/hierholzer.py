from dataclasses import dataclass

@dataclass
class Edge:
    i: int
    j: int
    cost: int | None = None

    def reverse(self):
        return Edge(self.j, self.i, self.cost)
    
@dataclass
class Adj:
    j: int
    cost: int | None = None
    edge: Edge | None = None
    idx: int = -1

    def iter(self):
        yield self.j
        yield self.cost
        yield self.edge
        yield self.idx

def is_connected(n: int, edges: list[Edge], adj_list: dict[int, list[Adj]]):
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

    return len(visited) == len(adj_list)

def make_adj_list(n: int, edges: list[Edge]):
    adj_list: dict[int, list[Adj]] = {i: [] for i in range(n)}

    for edge_idx, edge in enumerate(edges):
        adj_list[edge.i].append(Adj(j=edge.j, cost=edge.cost, edge=edge, idx=edge_idx))
        adj_list[edge.j].append(Adj(j=edge.i, cost=edge.cost, edge=edge, idx=edge_idx))

    return adj_list

def _find_eulerian_path(n: int, edges: list[Edge], s: int, t: int):
    adj = make_adj_list(n, edges)

    used_edges = [False]*len(edges)
    rem_path: list[Adj] = []

    def consume_path(i: int, t: int):
        # consume a path at i, then expect to finish at t
        # "just walk"
        path: list[Adj] = []
        while adj[i]:
            a = adj[i].pop()
            if not used_edges[a.idx]:
                used_edges[a.idx] = True
                path.append(a)
                i = a.j # "then walk 1 edge"

        # append those edges to rem_path
        while path:
            rem_path.append(path.pop())

        # from here we have finally reached s to t
        assert i == t

    # take any path from s to t
    consume_path(s, t)

    # now, remaining CCs are connected components, with all degrees even
    eul_path: list[Adj] = [Adj(s)]
    while rem_path:
        i = eul_path[-1].j # WALK ONCE

        # consume an eulerian cycle on the component containing i # WALK EVERYWHERE SHT
        consume_path(i, i)

        eul_path.append(rem_path.pop()) # BACKTRACK PARA MAVISIT NA UNG MGA EDGES

    edge_paths: list[Edge | None] = []
    for eul in eul_path:
        edge_paths.append(eul.edge)

    node_paths: list[int] = []
    for eul in eul_path:
        node_paths.append(eul.j)

    return eul_path

def find_eulerian_path(n: int, edges: list[Edge]):
    # assumes graph is connected

    # compute degrees
    deg = [0]*n
    for edge in edges:
        deg[edge.i] += 1
        deg[edge.j] += 1

    odd_nodes = [i for i in range(n) if deg[i] % 2]

    assert len(odd_nodes) % 2 == 0 # the number of odd nodes are always even

    if len(odd_nodes) <= 2: # meaning there's an eulerian path
        return _find_eulerian_path(n, edges, *(odd_nodes[:2] or (0, 0)))
    
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