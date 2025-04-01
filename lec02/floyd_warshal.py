from utils import Edge
from typing import TypeVar
from math import inf

T = TypeVar("T")

def make_adj_matrix(nodes: list[T], edges: list[Edge[T]], n: int, directed: bool = False, ) -> list[list[float]]:
    adj_matrix = [[inf] * n for _ in range(n)]

    node = {node: i for i, node in enumerate(nodes)} # setup index for each node T

    print(node)

    # diagonal should be 0
    for i in range(n):
        adj_matrix[i][i] = 0

    for edge in edges:
        adj_matrix[node[edge.x]][node[edge.y]] = min(adj_matrix[node[edge.x]][node[edge.y]], edge.weight)
        if not directed:
            adj_matrix[node[edge.y]][node[edge.x]] = min(adj_matrix[node[edge.y]][node[edge.x]], edge.weight)

    for adj in adj_matrix:
        print(adj)

    return adj_matrix

def apsp_floyd_warshall(nodes: list[T], edges: list[Edge[T]]):
    n = len(nodes)
    d = make_adj_matrix(nodes, edges, n)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] < inf and d[k][j] < inf:
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])

    print()
    for adj in d:
        print(adj)

    # detect negative weight cycle
    for i in range(n):
        for j in range(n):
            if d[i][j] < 0:
                print("Negative weight cycle detected!")
                return None

    return d

print(apsp_floyd_warshall([0, 1, 2, 3, 4], [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ]))
print()

print(apsp_floyd_warshall([0, 1, 2, 3, 4, 5, 6, 7], [
        Edge(0, 1, 2),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(4, 5, 1),
        Edge(5, 6, 1),
        Edge(0, 7, 1),
        Edge(7, 6, 7),
    ]))
print()

print(apsp_floyd_warshall([1, 2, 3, 4], [
        Edge(1, 2, 4),
        Edge(2, 3, 3),
        Edge(4, 3, 1),
        Edge(1, 4, 1),
        Edge(4, 2, 2),
        Edge(3, 1, 6),
]))
print()

print(apsp_floyd_warshall([1, 2, 3], [
        Edge(1, 2, 2),
        Edge(2, 3, 2),
        Edge(3, 1, 6)
]))
print()