from dataclasses import dataclass
import sys

@dataclass
class Edge:
    i: int
    j: int
    cost: int | None = None


def make_adj_list(n: int, edges: list[Edge]):
    adj_list: dict[int, list[tuple[int, int | None, Edge]]] = {i: [] for i in range(n + 1)}

    for edge in edges:
        adj_list[edge.i].append((edge.j, edge.cost, edge))
        adj_list[edge.j].append((edge.i, edge.cost, edge))

    return adj_list


def bridges_and_artic_pts(n: int, edges: list[Edge]):
    adj = make_adj_list(n, edges)

    vis = [-1]*(n+1)
    low = [-1]*(n+1)

    time = 0

    def visit(i: int):
        nonlocal time
        assert vis[i] == -1
        vis[i] = time
        time += 1

    bridges: list[Edge] = []
    artic_pts: list[int] = []

    def dfs(i: int, parent_edge: Edge | None):
        visit(i)

        is_root = parent_edge is None

        low[i] = vis[i]

        found_isolated_child = False
        children = 0

        for j, *_, edge in adj[i]:
            if vis[j] == -1:
                # tree edge
                dfs(j, edge)
                low[i] = min(low[i], low[j])

                children += 1

                if low[j] > vis[i]:
                    # bridge
                    bridges.append(edge)
                if low[j] >= vis[i]:
                    found_isolated_child = True

            elif edge is not parent_edge:
                # back edge
                low[i] = min(low[i], vis[j])

        if (not is_root and found_isolated_child) or (is_root and children >= 2):
            artic_pts.append(i)

    if n > 0:
        dfs(1, None)

    return bridges


N, M = map(int, sys.stdin.readline().split())
edges: list[Edge] = []

for _ in range(M):

    i, j = map(int, sys.stdin.readline().split())

    edges.append(Edge(i, j, None))


bridges = bridges_and_artic_pts(N, edges)

if len(bridges) == 1:
    print("YES")
else:
    print("NO")