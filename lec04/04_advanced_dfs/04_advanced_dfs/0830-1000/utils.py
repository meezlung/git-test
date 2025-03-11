# type: ignore
from collections.abc import Sequence

from dataclasses import dataclass

from random import Random

INF = float('inf')


@dataclass(order=True)
class Edge:
    i: int
    j: int
    cost: int | None = None


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



    def random_tree(self, n):
        return self.shuffled(self._random_tree(n))

    def _random_tree(self, n):
        nodes = self.shuffled(range(n))
        for i in range(1, n):
            j = self.randrange(i)
            i, j = self.shuffled((i, j))
            yield Edge(nodes[i], nodes[j])

    def random_graph(self, n, e):
        def rand_edge():
            i, j = self.choices(range(n), k=2)
            return Edge(i, j)

        edges = [rand_edge() for _ in range(e)]
        assert len(edges) == e
        return edges


    def random_connected_graph(self, n, e):
        if n == 0:
            return []

        assert e >= n - 1 >= 0

        edges = self.random_graph(n, e - (n - 1))

        # add a random tree
        edges += self.random_tree(n)

        assert len(edges) == e
        return self.shuffled(edges)


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
