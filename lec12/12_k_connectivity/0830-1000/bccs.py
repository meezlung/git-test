# type: ignore

from utils import make_adjacency_list, Edge


def bridges_articulation_points_and_bccs(n, edges):

    if any(edge.i == edge.j for edge in edges):
        raise NotImplementedError("self-loops not supported")

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
    edge_visited = [False]*len(edges)
    edge_stack = []
    bccs = []
    def extract_bcc(edge):
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
                    # found BCC!
                    bccs.append(list(extract_bcc(edge)))
                    found_isolated_child = True

            elif edge is not parent_edge:
                # back edge
                edge_stack.append(edge)
                low[i] = min(low[i], vis[j])

        if not is_root and found_isolated_child or is_root and children >= 2:
            artic_points.append(i)

    if n > 0:
        dfs(0, None)

    return bridges, artic_points, bccs


if __name__ == '__main__':
    from pprint import pprint

    pprint(bridges_articulation_points_and_bccs(10, (
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
