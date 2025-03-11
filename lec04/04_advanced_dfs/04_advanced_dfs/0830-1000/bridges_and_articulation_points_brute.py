# type: ignore

from utils import make_adjacency_list, Edge


def is_connected(n, edges, *, ignored_node=-1):
    adj = make_adjacency_list(n, edges)
    vis = [False]*n
    def dfs(i):
        assert not vis[i]
        vis[i] = True

        for j, *_ in adj[i]:
            if not vis[j]:
                dfs(j)

    for s in range(n):
        if s != ignored_node:
            dfs(s)
            break

    return all(vis[i] for i in range(n) if i != ignored_node)


def bridges_and_articulation_points(n, edges):

    assert is_connected(n, edges)

    bridges = []
    for edge in edges:
        new_edges = [*edges]
        new_edges.remove(edge)
        if not is_connected(n, new_edges):
            bridges.append(edge)


    artic_points = []
    for i in range(n):
        new_edges = [edge for edge in edges if i not in (edge.i, edge.j)]
        if not is_connected(n, new_edges, ignored_node=i):
            artic_points.append(i)

    return bridges, artic_points


if __name__ == '__main__':
    # print(*bridges(6, (
    #         Edge(0, 1),
    #         Edge(0, 2),
    #         Edge(2, 1),
    #         Edge(2, 3),
    #         Edge(4, 5),
    #         Edge(1, 4),
    #     )))



    print(*bridges_and_articulation_points(10, (
            Edge(0, 1),
            Edge(0, 2),
            Edge(2, 1),
            Edge(2, 3),
            Edge(4, 5),
            Edge(1, 4),
            Edge(5, 6),
            Edge(5, 7),
            Edge(5, 8),
            Edge(5, 9),
            Edge(6, 7),
            Edge(8, 9),
        )))
