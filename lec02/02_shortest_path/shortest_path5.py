# type: ignore

from heapq import heappush, heappop

from utils import make_adjacency_list, Edge, INF


def shortest_paths_from(n, edges, x):
    # Dijkstra's algorithm
    adj = make_adjacency_list(n, edges, directed=True)

    visited = [False]*n
    dists = [INF]*n

    pq = []

    heappush(pq, (0, x))

    ans = 0
    while pq:
        (cost, i) = heappop(pq)

        if visited[i]:
            continue

        visited[i] = True
        dists[i] = cost

        for j, c, edge in adj[i]:
            heappush(pq, (cost + c, j))

    return dists


def shortest_paths(n, edges):
    return [shortest_paths_from(n, edges, x) for x in range(n)]


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
