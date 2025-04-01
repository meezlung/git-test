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

    def random_set_ops(self):
        return list(self._random_set_ops())

    def _random_set_ops(self):
        q = self.randint(1, self.choice([3, 11, 31, 111, 311, 1111]))
        # q = 100000

        prob_insert = self.uniform(0.0, 0.1**self.randint(0, 3))
        setc = 0
        for _ in range(q):
            # if setc == 0:
            if setc == 0 or self.random() < prob_insert:
                yield 'make',
                setc += 1
            else:
                idx = self.randrange(setc)
                # val = self.randint(1, self.choice([3, 11]))
                val = self.getrandbits(128)
                op = self.choice(['add', 'remove', 'contains'])
                # op = self.choice(['add'])
                yield op, idx, val




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
