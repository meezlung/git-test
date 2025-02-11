from dataclasses import dataclass
import sys

@dataclass
class Edge:
    i: int
    j: int


def make_adj_list(n: int, edges: list[Edge]):
    adj_list: dict[int, list[tuple[int, Edge]]] = {i: [] for i in range(n + 1)}

    for edge in edges:
        adj_list[edge.i].append((edge.j, edge))

    return adj_list


def sccs(n: int, edges: list[Edge]):
    adj = make_adj_list(n, edges)

    vis: list[bool] = [False] * (n + 1)

    def dfs(i: int, adj: dict[int, list[tuple[int, Edge]]], stack: list[int]):
        # before visiting i
        assert not vis[i]
        vis[i] = True
        
        for j, *_ in adj[i]:
            if not vis[j]:
                dfs(j, adj, stack)

        # after i's expansion
        stack.append(i)

    stack: list[int] = []
    for x in range(1, n + 1):
        if not vis[x]:
            dfs(x, adj, stack)

    jda = make_adj_list(n, [
        Edge(edge.j, edge.i) for edge in edges
    ])

    vis: list[bool] = [False] * (n + 1)

    while stack:
        i = stack.pop()
        if not vis[i]:
            scc: list[int] = []
            dfs(i, jda, scc)
            yield scc


n, m = map(int, sys.stdin.readline().split())

edges: list[Edge] = []

for _ in range(m):
    i, j = map(int, sys.stdin.readline().split())
    edges.append(Edge(i, j))

kingdoms = [*sccs(n, edges)]

kingdom_num = 0

answers: list[int] = []

collect_ans: list[tuple[int, int]] = []

num = 0

component_map = [0] * (n + 1)

for i, kd in enumerate(kingdoms, start=1):
    for k in kd:
        component_map[k] = i

    num += 1


print(num)
print(" ".join(map(str, component_map[1:])))