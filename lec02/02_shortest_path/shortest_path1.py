# type: ignore

from functools import cache

from utils import make_adjacency_list, Edge

INF = float('inf')

def shortest_paths_to(n, edges, x):

    adj = make_adjacency_list(n, edges, directed=True)

    @cache
    def d(i, t):
        # shortest path from i to x with at most t edges
        assert t >= 0
        if i == x:
            return 0
        elif t == 0:
            return INF
        else:
            return min((c + d(j, t - 1) for j, c, _ in adj[i]), default=INF)

    return [d(i, n) for i in range(n)]


def shortest_paths(n, edges):
    dists = [shortest_paths_to(n, edges, x) for x in range(n)]

    return [[dists[j][i] for j in range(n)] for i in range(n)]


if __name__ == '__main__':

    for row in shortest_paths(5, [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ]):
        print(row)
    # exit()


    for row in shortest_paths(9, [
        Edge(0, 1, 2),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(4, 5, 1),
        Edge(5, 6, 1),
        Edge(0, 7, 1),
        Edge(7, 6, 7),
    ]):
        print(row)
    # exit()

    print(shortest_paths_to(9, [
        Edge(0, 1, 2),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(4, 5, 1),
        Edge(5, 6, 1),
        Edge(0, 7, 1),
        Edge(7, 6, 7),
    ], 8))


    print(shortest_paths_to(5, [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ], 4))

    # G1 = {
    #     0: [(2, 1), (1, 7)],
    #     1: [(1, 2)],
    #     2: [(1, 3)],
    #     3: [(1, 4)],
    #     4: [(1, 5)],
    #     5: [(1, 6)],
    #     6: [],
    #     7: [(7, 6)]
    # }