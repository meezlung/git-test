# type: ignore
from itertools import product

from utils import Edge, make_adjacency_list

def sccs(n, edges):
    adj = make_adjacency_list(n, edges, directed=True)

    vis = [False]*n
    def dfs(i, adj, stack):
        assert not vis[i]
        vis[i] = True
        for j, *_ in adj[i]:
            if not vis[j]:
                dfs(j, adj, stack)

        # finish na si i
        stack.append(i)




    # - for each node x:
    #     if x is not visited:
    #         DFS from x
    stack = []
    for x in range(n):
        if not vis[x]:
            dfs(x, adj, stack)
    # - ^ keep track of finishing times

    # - reverse the graph
    jda = make_adjacency_list(n, [
            Edge(edge.j, edge.i)
            for edge in edges
        ], directed=True)

    vis = [False]*n
    # - for each node x in DECREASING finishing time:
    #     if x is not visited:
    #         DFS from x
    #         all nodes visited here constitute an SCC
    while stack:
        i = stack.pop()
        if not vis[i]:
            scc = []
            dfs(i, jda, scc)
            yield scc


if __name__ == '__main__':
    print(*sccs(4, [
        Edge(0, 1),
        Edge(1, 3),
        Edge(3, 0),
        Edge(3, 2),
    ]))
