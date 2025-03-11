# type: ignore

from collections.abc import Sequence

from dataclasses import dataclass

from random import Random

INF = float('inf')


@dataclass
class Edge:
    i: int
    j: int
    cost: int


class CS33Random(Random):
    def shuffled(self, seq):
        seq = [*seq]
        self.shuffle(seq)
        return seq


def make_adjacency_list(n: int, edges: Sequence[Edge], *, directed=False) -> list[list[tuple[int, int, Edge]]]:
    adj = [[] for _ in range(n)]

    def add_edge(i, j, cost, edge):
        adj[i].append((j, cost, edge))

    for edge in edges:
        add_edge(edge.i, edge.j, edge.cost, edge)
        if not directed:
            add_edge(edge.j, edge.i, edge.cost, edge)

    return adj


def make_adjacency_matrix(n: int, edges: Sequence[Edge], *, directed=False):
    mat = [[INF]*n for i in range(n)]

    def add_edge(i, j, cost, edge):
        mat[i][j] = min(mat[i][j], cost)

    for edge in edges:
        add_edge(edge.i, edge.j, edge.cost, edge)
        if not directed:
            add_edge(edge.j, edge.i, edge.cost, edge)

    return mat
