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
        add_edge(edge.j, edge.i, edge.cost, edge)

    return adj_list


def bridges_and_articulation_points(n: int, edges: list[Edge]):

    adj = make_adj_list(n, edges)

    vis = [-1] * n
    low = [-1] * n
    
    time = 0

    def visit(i: int):
        nonlocal time
        assert vis[i] == -1
        vis[i] = time
        time += 1

    bridges: list[Edge] = []
    artic_pts: list[int]= []

    def dfs(i: int, parent_edge: Edge | None):
        visit(i)

        is_root = parent_edge is None

        low[i] = vis[i]

        found_isolated_child = False
        children = 0

        for j, *_, edge in adj[i]:
            if vis[j] == -1:
                dfs(j, edge)
                low[i] = min(low[i], low[j])
                children += 1

                if low[j] > vis[i]:
                    # bridge
                    bridges.append(edge)
                
                if low[j] >= vis[i]:
                    found_isolated_child = True

            elif edge is not parent_edge:
                low[i] = min(low[i], vis[j])

        if (not is_root and found_isolated_child) or (is_root and children >= 2):
            artic_pts.append(i)

    if n > 0:
        dfs(0, None)

    return bridges, artic_pts



if __name__ == '__main__':
    print(*bridges_and_articulation_points(10, [
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
    ]))

