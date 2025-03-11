# type: ignore

from utils import make_adjacency_list, Adj, Edge


def _find_eulerian_path(n, edges, s, t):
    adj = make_adjacency_list(n, edges, directed=False)

    used_edge = [False]*len(edges)  # this is only needed for the undirected case
    rem_path = []

    def consume_path(i, t):
        # "consume" a path from i, and then expect to finish at t
        path = []
        while adj[i]:
            a = adj[i].pop()
            if not used_edge[a.idx]:
                used_edge[a.idx] = True
                path.append(a)
                i = a.j

        # append those edges to rem_path
        while path:
            rem_path.append(path.pop())

        assert i == t

    # take any path from s to t
    consume_path(s, t)

    # now, remaining CCs are connected components with all degrees even


    eul_path = [Adj(s)]
    while rem_path:
        i = eul_path[-1].j

        # consume an eulerian cycle on the component containing i
        consume_path(i, i)

        # then go to the next edge
        eul_path.append(rem_path.pop())

    return eul_path


def find_eulerian_path(n, edges):
    # assumes graph is connected

    # compute degrees
    deg = [0]*n
    for edge in edges:
        deg[edge.i] += 1
        deg[edge.j] += 1
    odd_nodes = [i for i in range(n) if deg[i] % 2]
    assert len(odd_nodes) % 2 == 0

    if len(odd_nodes) <= 2:
        return _find_eulerian_path(n, edges, *(odd_nodes[:2] or (0, 0)))


print(find_eulerian_path(5, [
    Edge(0, 1),
    Edge(1, 2),
    Edge(2, 3),
    Edge(3, 4),
    Edge(4, 0),
    Edge(0, 3),
    Edge(1, 4),
    Edge(1, 3),
]))