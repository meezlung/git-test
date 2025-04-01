# type: ignore

from dataclasses import dataclass
from collections import deque
from collections.abc import Sequence

@dataclass
class Edge:
    i: int
    j: int
    cost: int = 1

def make_adj_list(n: int, edges: list[Edge]):
    adj: dict[int, list[tuple[int, int, int, Edge]]] = {i: [] for i in range(n)}
    for edge_idx, edge in enumerate(edges):
        adj[edge.i].append((edge.j, edge.cost, edge_idx, edge))
        adj[edge.j].append((edge.i, edge.cost, edge_idx, edge))
    return adj

def is_connected(adj: dict[int, list[tuple[int, int, int, Edge]]]):
    visited: set[int] = set()
    def dfs(node: int):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for neighbor, *_ in adj[current]:
                    stack.append(neighbor)
    start_node = next((node for node in adj if adj[node]), None)
    if start_node is None:
        return True  # if all nodes are isolated
    dfs(start_node)
    return len(visited) == sum(1 for node in adj if adj[node])

def bridges_articulation_points_and_bccs(n: int, edges: list[Edge]):
    if any(edge.i == edge.j for edge in edges):  # self loops
        raise NotImplementedError("self loops are not supported")
    
    adj = make_adj_list(n, edges)
    if not is_connected(adj):
        raise ValueError("Graph not connected")
    
    vis = [-1] * n
    low = [-1] * n
    time = 0

    bridges = []
    artic_pts = []
    edge_visited = [False] * len(edges)
    edge_stack = []
    bccs = []

    def extract_bcc(edge):
        while True:
            last_edge = edge_stack.pop()
            yield last_edge
            if last_edge == edge:
                return edge

    def dfs(i, parent_edge):
        nonlocal time
        # visit node i
        assert vis[i] == -1
        vis[i] = time
        low[i] = time
        time += 1
        is_root = (parent_edge is None)
        children = 0
        found_isolated_child = False

        for j, *_ , edge_idx, edge in adj[i]:
            if edge_visited[edge_idx]:
                continue
            edge_visited[edge_idx] = True
            if vis[j] == -1:
                edge_stack.append(edge)
                children += 1
                dfs(j, edge)
                low[i] = min(low[i], low[j])
                if low[j] > vis[i]:
                    bridges.append(edge)
                if low[j] >= vis[i]:
                    bccs.append(list(extract_bcc(edge)))
                    found_isolated_child = True
            elif edge is not parent_edge:
                edge_stack.append(edge)
                low[i] = min(low[i], vis[j])
        if (not is_root and found_isolated_child) or (is_root and children >= 2):
            artic_pts.append(i)

    if n > 0:
        dfs(0, None)
    return bccs

def max_production(
        conveyor_belts: Sequence[tuple[int, int]],
        complexities: Sequence[int],
    ) -> tuple[int, list[tuple[int, int]]]:

    n = len(complexities)
    m = len(conveyor_belts)
    
    # Create Edge objects (convert input 1-indexed to 0-indexed)
    edges = []
    for a, b in conveyor_belts:
        edges.append(Edge(a - 1, b - 1))
    
    # Use your BCC finder to get bccs.
    bccs = bridges_articulation_points_and_bccs(n, edges)
    
    # Determine which edges are bridges.
    # Here, if a bcc contains exactly one edge, we treat that edge as a bridge.
    is_bridge = [False] * m
    for bcc in bccs:
        if len(bcc) == 1:
            e = bcc[0]
            # Find its index in our original edges list.
            idx = edges.index(e)
            is_bridge[idx] = True

    # DSU for union–find on non–bridge edges.
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    # Union vertices connected by non–bridge edges.
    for idx, e in enumerate(edges):
        if not is_bridge[idx]:
            union(e.i, e.j)
    
    # For each vertex, find its component id.
    comp = [find(i) for i in range(n)]
    # Compute total complexity for each component.
    comp_sum = {}
    comp_vertices = {}
    for v in range(n):
        cid = comp[v]
        comp_sum[cid] = comp_sum.get(cid, 0) + complexities[v]
        comp_vertices.setdefault(cid, []).append(v)
    
    # Choose best component (sink) as the one with maximum total complexity.
    best_comp = max(comp_sum, key=comp_sum.get)
    if len(comp_sum) == 1:
        prod_value = sum(complexities)
    else:
        prod_value = comp_sum[best_comp]
    
    # Build the bridge graph on the component level.
    comp_graph = {cid: set() for cid in comp_sum}
    for idx, e in enumerate(edges):
        if is_bridge[idx]:
            cu, cv = find(e.i), find(e.j)
            comp_graph[cu].add(cv)
            comp_graph[cv].add(cu)
    
    # BFS from best_comp on the component-level bridge graph.
    INF = 10**9
    dist = {cid: INF for cid in comp_sum}
    dq = deque()
    dist[best_comp] = 0
    dq.append(best_comp)
    while dq:
        cur = dq.popleft()
        for nb in comp_graph[cur]:
            if dist[nb] > dist[cur] + 1:
                dist[nb] = dist[cur] + 1
                dq.append(nb)
    
    # Prepare an array to hold orientations (in 0-indexed form).
    oriented = [None] * m

    # For each bridge edge, orient it toward the best component.
    for idx, e in enumerate(edges):
        if is_bridge[idx]:
            cu, cv = find(e.i), find(e.j)
            # Orient from the vertex in the component with larger distance to the one with smaller distance.
            if dist[cu] > dist[cv]:
                oriented[idx] = (e.i, e.j)
            else:
                oriented[idx] = (e.j, e.i)
    
    # For non–bridge edges, assign an arbitrary orientation that makes each component strongly connected.
    # Build a graph (for non–bridge edges) for each vertex.
    nb_graph = {v: [] for v in range(n)}
    for idx, e in enumerate(edges):
        if not is_bridge[idx]:
            nb_graph[e.i].append((e.j, idx))
            nb_graph[e.j].append((e.i, idx))
    
    non_bridge_used = [False] * m
    visited_nb = [False] * n
    def dfs_nb(u):
        visited_nb[u] = True
        for v, edge_idx in nb_graph[u]:
            if non_bridge_used[edge_idx]:
                continue
            non_bridge_used[edge_idx] = True
            # Assign orientation from u to v.
            oriented[edge_idx] = (u, v)
            if not visited_nb[v]:
                dfs_nb(v)
    # Run DFS for each union–find component separately.
    for cid, vertices in comp_vertices.items():
        for v in vertices:
            if not visited_nb[v]:
                dfs_nb(v)
    
    # Convert oriented edges back to 1-indexed.
    final_oriented = [(u + 1, v + 1) for (u, v) in oriented]
    return prod_value, final_oriented
