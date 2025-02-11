from dataclasses import dataclass
from typing import TypeVar, Generic
from math import inf
T = TypeVar("T")

@dataclass
class Edge(Generic[T]):
    x: T
    y: T
    weight: int

def make_adj_matrix(nodes: list[T], edges: list[Edge[T]], n: int, directed: bool = False) -> list[list[float]]:
    adj_matrix = [[inf]*n for _ in range(n)]
    node_idx = {node: i for i, node in enumerate(nodes)}

    # diagonal should be 0
    for i in range(n):
        adj_matrix[i][i] = 0

    # fill in edge relation
    for edge in edges:
        adj_matrix[node_idx[edge.x]][node_idx[edge.y]] = min(adj_matrix[node_idx[edge.x]][node_idx[edge.y]], edge.weight)
        if not directed:
            adj_matrix[node_idx[edge.y]][node_idx[edge.x]] = min(adj_matrix[node_idx[edge.y]][node_idx[edge.x]], edge.weight)

    return adj_matrix

def floyd_warshall(nodes: list[T], edges: list[Edge[T]]) -> list[list[float]] | None:
    n = len(nodes)
    d = make_adj_matrix(nodes, edges, n)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] < inf and d[k][j] < inf:
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    
    # detect negative weight cycles
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] < 0:
                    print("Negative weight cycle...")
                    return None

    return d



