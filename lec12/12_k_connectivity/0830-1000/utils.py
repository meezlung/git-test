# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass
from math import inf
from random import Random


@dataclass
class Edge:
    i: int
    j: int
    cost: int = 1


class CS33Random(Random):
    def shuffled(self, seq):
        seq = [*seq]
        self.shuffle(seq)
        return seq

    def random_persistent_stack_ops(self):
        return list(self._random_persistent_stack_ops())

    def _random_persistent_stack_ops(self):
        q = self.randint(1, self.choice([3, 11, 31, 111, 311, 1111]))
        V = self.randint(1, self.choice([3, 11, 31, 111, 311, 1111]))

        prob_make = self.uniform(0.0, 0.1**self.randint(0, 3))
        stack_h_sizes = []
        for _ in range(q):
            if not stack_h_sizes or self.random() < prob_make:
                stack_h_sizes.append(1)
                yield 'make',
            else:
                idx = self.randrange(len(stack_h_sizes))
                match self.randrange(4):
                    case 0:
                        # push
                        val = self.randint(0, V)
                        yield 'push', idx, val
                        stack_h_sizes[idx] += 1
                    case 1:
                        # pop
                        yield 'pop', idx
                        stack_h_sizes[idx] += 1
                    case 2:
                        # len
                        yield 'len', idx
                    case 3:
                        # revert
                        ridx = self.randrange(stack_h_sizes[idx])
                        yield 'revert', idx, ridx
                        stack_h_sizes[idx] += 1
                    case _:
                        raise ValueError

    def random_persistent_set_ops(self):
        return list(self._random_persistent_set_ops())

    def _random_persistent_set_ops(self):
        q = self.randint(1, self.choice([3, 11, 31, 111, 311, 1111]))
        V = self.randint(1, self.choice([3, 11, 31, 111, 311, 1111]))

        prob_make = self.uniform(0.0, 0.1**self.randint(0, 3))
        set_histories = []
        for _ in range(q):
            if not set_histories or self.random() < prob_make:
                set_histories.append([set()])
                yield 'make',
            else:
                idx = self.randrange(len(set_histories))
                match self.randrange(3):
                    case 0:
                        # push
                        val = self.randint(0, V)
                        yield 'add', idx, val
                        set_histories[idx].append(set_histories[idx][-1] | {val})
                    case 1:
                        # contains
                        val = self.randint(0, V)
                        yield 'contains', idx, val
                    case 2:
                        # revert
                        ridx = self.randrange(len(set_histories[idx]))
                        yield 'revert', idx, ridx
                        set_histories[idx].append(set_histories[idx][ridx])
                    case _:
                        raise ValueError

    def random_set_ops(self):
        return list(self._random_set_ops())

    def _random_set_ops(self):
        q = self.randint(1, self.choice([3, 11, 31, 111, 311, 1111]))
        # q = 100000

        prob_make = self.uniform(0.0, 0.1**self.randint(0, 3))
        setc = 0
        for _ in range(q):
            # if setc == 0:
            if setc == 0 or self.random() < prob_make:
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

    def add_edge(i, j, cost, edge_idx, edge):
        adj[i].append((j, cost, edge_idx, edge))

    for edge_idx, edge in enumerate(edges):
        add_edge(edge.i, edge.j, edge.cost, edge_idx, edge)
        if not directed:
            add_edge(edge.j, edge.i, edge.cost, edge_idx, edge)

    return adj


def make_adjacency_matrix(n: int, edges: Sequence[Edge], *, directed=False):
    mat = [[inf]*n for i in range(n)]

    def add_edge(i, j, cost, edge):
        mat[i][j] = min(mat[i][j], cost)

    for edge in edges:
        add_edge(edge.i, edge.j, edge.cost, edge)
        if not directed:
            add_edge(edge.j, edge.i, edge.cost, edge)

    return mat
