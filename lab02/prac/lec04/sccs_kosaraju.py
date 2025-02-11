
from dataclasses import dataclass


@dataclass
class Edge:
    i: int
    j: int
    cost: int | None = None

def make_adj_list(n: int, edges: list[Edge]) -> list[list[tuple[int, int | None, Edge]]]:
    adj_list: list[list[tuple[int, int | None, Edge]]] = [[] for _ in range(n)]

    def add_edge(i: int, j: int, cost: int | None, edge: Edge):
        adj_list[i].append((j, cost, edge))

    
    for edge in edges:
        add_edge(edge.i, edge.j, edge.cost, edge)

    return adj_list


def sccs(n: int, edges: list[Edge]):
    adj: list[list[tuple[int, int | None, Edge]]] = make_adj_list(n, edges)

    vis: list[bool] = [False] * n
    
    def dfs(i: int, adj: list[list[tuple[int, int | None, Edge]]], stack: list[int]):
        # before
        assert not vis[i]
        vis[i] = True

        # loop
        for j, *_ in adj[i]:
            if not vis[j]:
                dfs(j, adj, stack)

        # after expansion
        stack.append(i)


    stack: list[int] = []
    for x in range(n):
        if not vis[x]:
            dfs(x, adj, stack)

    
    jda = make_adj_list(n, [
        Edge(edge.j, edge.i) for edge in edges
    ])

    vis: list[bool] = [False] * n

    while stack:
        i = stack.pop()
        if not vis[i]:
            scc: list[int] = []
            dfs(i, jda, scc)
            yield scc


if __name__ == '__main__':
    print(*sccs(4, [
        Edge(0, 1),
        Edge(1, 3),
        Edge(3, 0),
        Edge(3, 2),
    ]))