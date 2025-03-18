# type: ignore

from dataclasses import dataclass

@dataclass
class Edge:
    i: int
    j: int
    cost: int = 1

def make_adj_list(n: int, edges: list[Edge]):
    adj: dict[int, list[tuple[int, int, int, Edge]]] = {i: [] for i in range(n + 1)}

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
        # if all nodes are isolated
        return True
    
    dfs(start_node)

    return len(visited) == sum(1 for node in adj if adj[node])

def bridges_articulation_points_and_bccs(n: int, edges: list[Edge]):
    
    if any(edge.i == edge.j for edge in edges):
        raise NotImplementedError("self loops are not supported")
    
    adj = make_adj_list(n, edges)

    if not is_connected(adj):
        return "NO"
    
    low = [-1] * n
    vis = [-1] * n

    time = 0
    def visit(i):
        nonlocal time
        assert vis[i] == -1
        vis[i] = time
        time += 1
    
    bridges = []
    artic_pts = []
    edge_visited = [False] * len(edges)
    edge_stack = []
    bccs = []

    def extract_bccs(edge):
        # pop until edge is popped
        while True:
            last_edge = edge_stack.pop()
            yield last_edge
            if last_edge == edge:
                return
            
    
    def dfs(i, parent_edge):
        visit(i)
        is_root = parent_edge is None
        low[i] = vis[i]
        found_isolated_child = False
        children = 0 

        for j, *_, edge_idx, edge in adj[i]:

            if edge_visited[edge_idx]:
                continue

            edge_visited[edge_idx] = True

            if vis[j] == -1:
                # tree edge
                edge_stack.append(edge)
                dfs(j, edge)
                low[i] = min(low[i], low[j])

                children += 1

                if low[j] > vis[i]:
                    # this is a bridge
                    bridges.append(edge)

                if low[j] >= vis[i]:
                    # we have found our BCC
                    bccs.append(list(extract_bccs(edge)))
                    found_isolated_child = True

            elif edge is not parent_edge:
                # this is a back edge
                edge_stack.append(edge)
                low[i] = min(low[i], vis[j])

        if (not is_root and found_isolated_child) or (is_root and children >= 2):
            artic_pts.append(i)

        
    if n > 0:
        dfs(0, None)

    return bridges


def can_make_all_pairs_good(n: int, edges: list[Edge]) -> str:
    bridges = bridges_articulation_points_and_bccs(n, edges)

    # no bridges -> Already good
    if not bridges:
        return "YES"

    # if there's exactly one bridge, check if adding one edge can fix it
    if len(bridges) == 1:
        u, v = bridges[0].i, bridges[0].j

        # Adding (u, v) as an extra edge will fix the bridge
        new_edge = Edge(u, v)

        # Add the new edge to the graph and check if it's now 2-edge-connected
        new_edges = edges + [new_edge]
        new_bridges = bridges_articulation_points_and_bccs(n, new_edges)

        # If no bridges after adding the edge, graph becomes 2-edge-connected
        if not new_bridges:
            return "YES"

    # If there are multiple bridges, adding one edge can't fix it
    return "NO"

if __name__ == '__main__':
    import sys

    N, M = map(int, sys.stdin.readline().split())
    edges: list[Edge] = []

    for _ in range(M):

        i, j = map(int, sys.stdin.readline().split())

        edges.append(Edge(i, j, None))

    print(can_make_all_pairs_good(N, edges))