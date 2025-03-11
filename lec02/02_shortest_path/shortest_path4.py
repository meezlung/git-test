# type: ignore

from utils import make_adjacency_matrix, Edge, INF


def shortest_paths(n, edges):
    # Floyd's algorithm
    mat = make_adjacency_matrix(n, edges, directed=True)

    d = [[INF]*n for j in range(n)]


    for i in range(n):
        for j in range(n):
            d[i][j] = 0 if i == j else mat[i][j]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])

    return d


if __name__ == '__main__':
    for row in shortest_paths(5, [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ]):
        print(row)

    print()


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

    # print(shortest_paths_to(9, [
    #     Edge(0, 1, 2),
    #     Edge(1, 2, 1),
    #     Edge(2, 3, 1),
    #     Edge(3, 4, 1),
    #     Edge(4, 5, 1),
    #     Edge(5, 6, 1),
    #     Edge(0, 7, 1),
    #     Edge(7, 6, 7),
    # ], 8))


    # print(shortest_paths_to(5, [
    #     Edge(0, 1, 1),
    #     Edge(1, 2, 1),
    #     Edge(2, 3, 1),
    #     Edge(3, 4, 1),
    #     Edge(3, 1, 1),
    # ], 4))

    # # G1 = {
    # #     0: [(2, 1), (1, 7)],
    # #     1: [(1, 2)],
    # #     2: [(1, 3)],
    # #     3: [(1, 4)],
    # #     4: [(1, 5)],
    # #     5: [(1, 6)],
    # #     6: [],
    # #     7: [(7, 6)]
    # # }
