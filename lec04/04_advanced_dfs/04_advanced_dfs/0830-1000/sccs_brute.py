# type: ignore
from itertools import product

from utils import Edge

def sccs(n, edges):
    reach = [[i == j for j in range(n)] for i in range(n)]

    for edge in edges:
        reach[edge.i][edge.j] = True

    # Floyd's algorithm
    for k, i, j in product(range(n), repeat=3):
        reach[i][j] = reach[i][j] or reach[i][k] and reach[k][j]

    def is_strongly_connected(i, j):
        return reach[i][j] and reach[j][i]

    sccs = []
    vis = [False]*n
    for s in range(n):
        if not vis[s]:
            scc = [i for i in range(n) if is_strongly_connected(i, s)]
            for i in scc:
                vis[i] = True
            sccs.append(scc)

    return sccs

if __name__ == '__main__':
    print(*sccs(4, [
            Edge(0, 1),
            Edge(1, 3),
            Edge(3, 0),
            Edge(3, 2),
        ]))
