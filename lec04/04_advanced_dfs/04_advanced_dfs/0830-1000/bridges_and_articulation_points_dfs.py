# type: ignore
from utils import make_adjacency_list, Edge


def bridges_and_articulation_points(n, edges):

    # assert is_connected(n, edges)

    adj = make_adjacency_list(n, edges)

    vis = [-1]*n
    low = [-1]*n

    time = 0
    def visit(i):
        nonlocal time
        assert vis[i] == -1
        vis[i] = time
        time += 1

    bridges = []
    artic_points = []
    def dfs(i, parent_edge):
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
                    # this is a bridge
                    bridges.append(edge)

                if low[j] >= vis[i]:
                    found_isolated_child = True

            elif edge is not parent_edge:
                # back edge
                low[i] = min(low[i], vis[j])

        if not is_root and found_isolated_child or is_root and children >= 2:
            artic_points.append(i)

    if n > 0:
        dfs(0, None)

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

