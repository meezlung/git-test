# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass
from random import Random


@dataclass(frozen=True, order=True)
class Edge:
    i: int
    j: int
    cost: int | None = None

    def reverse(self):
        return Edge(self.j, self.i, self.cost)


class CS33Random(Random):
    def shuffled(self, seq):
        seq = [*seq]
        self.shuffle(seq)
        return seq


    def random_tree(self, n, *, weighted=True):
        nodes = self.shuffled(range(n))
        for i in range(1, n):
            j = self.randrange(i)
            i, j = self.shuffled((i, j))
            yield Edge(nodes[i], nodes[j], self.rand_cost(weighted=weighted))


    def rand_cost(self, *, weighted=True):
        if weighted:
            # positive costs
            return self.randint(1, self.choice([3, 11, 31, 111]))
        else:
            return None


    def random_graph(self, n, e, *, weighted=True):

        def rand_edge():
            i, j = self.choices(range(n), k=2)
            return Edge(i, j, self.rand_cost(weighted=weighted))

        edges = [rand_edge() for _ in range(e)]

        return self.shuffled(edges)

    def random_connected_graph(self, n, e, *, weighted=True):
        assert e >= n - 1
        edges = self.random_graph(n, e - (n - 1), weighted=weighted)

        # add a random tree
        edges += self.random_tree(n, weighted=weighted)

        assert len(edges) == e

        return self.shuffled(edges)


@dataclass(frozen=True)
class Adj:
    j: int
    cost: int | None = None
    edge: Edge | None = None
    idx: int = -1

    def __iter__(self):
        yield self.j
        yield self.cost
        yield self.edge
        yield self.idx


def make_adjacency_list(n: int, edges: Sequence[Edge], directed: bool = False) -> list[list[Adj]]:
    adj: list[list[Adj]] = [[] for _ in range(n)]

    for edge_idx, edge in enumerate(edges):
        adj[edge.i].append(Adj(j=edge.j, cost=edge.cost, edge=edge, idx=edge_idx))
        if not directed:
            adj[edge.j].append(Adj(j=edge.i, cost=edge.cost, edge=edge, idx=edge_idx))

    return adj




def make_adjacency_matrix(n: int, edges: Sequence[Edge], *, directed: bool = False):
    mat = [[INF]*n for i in range(n)]

    def add_edge(i, j, cost, edge):
        mat[i][j] = min(mat[i][j], cost)

    for edge in edges:
        add_edge(edge.i, edge.j, edge.cost, edge)
        if not directed:
            add_edge(edge.j, edge.i, edge.cost, edge)

    return mat


def simulate_set_ops(Set, operations):
    sets = []
    for typ, *data in operations:
        match typ:
            case 'make':
                sets.append(Set())
            case 'add':
                idx, v = data
                assert 0 <= idx < len(sets)
                yield sets[idx].add(v)
            case 'remove':
                idx, v = data
                assert 0 <= idx < len(sets)
                yield sets[idx].remove(v)
            case 'contains':
                idx, v = data
                assert 0 <= idx < len(sets)
                yield v in sets[idx]
            case 'next_larger':
                idx, v = data
                assert 0 <= idx < len(sets)
                yield sets[idx].next_larger(v)
            case 'len':
                idx, = data
                assert 0 <= idx < len(sets)
                yield len(sets[idx])
            case _:
                raise ValueError(f"unknown operation type: {typ}")


def make_set_ops(rand, n):
    V = rand.randint(1, rand.choice([3, 5, 7, 11, 31, 111, 311]))
    addprob = rand.random() if rand.random() < 0.2 else rand.uniform(0, 0.1)
    queprob = rand.random()
    setc = 0
    while True:
        if not setc or setc < n and rand.random() < 0.05:
            setc += 1
            yield 'make',
        else:
            idx = rand.randrange(setc)
            if rand.random() < queprob:
                op = rand.choice(['contains', 'next_larger']*3 + ['len'])
            else:
                op = 'add' if rand.random() < addprob else 'remove'
            if op != 'len':
                v = rand.randint(-V, V)
                yield op, idx, v
            else:
                yield op, idx


def is_connected(n, edges, *, nodes=None):
    adj = make_adjacency_list(n, edges, directed=False)

    vis = [False]*n
    def dfs(i):
        assert 0 <= i < n
        assert not vis[i]
        vis[i] = True
        for j, *_ in adj[i]:
            if not vis[j]:
                dfs(j)

    if nodes is None:
        nodes = range(n)

    if nodes:
        dfs(nodes[0])

    return all(vis[node] for node in nodes)


class UnionFind:
    def __init__(self, n):
        self.parent = [-1]*n
        self.rank = [1]*n
        super().__init__()

    def __getitem__(self, i):
        if self.parent[i] < 0:
            return i
        else:
            self.parent[i] = self[self.parent[i]]
            return self.parent[i]

    def union(self, i, j):
        if (i := self[i]) == (j := self[j]):
            return False

        if self.rank[i] == self.rank[j]:
            self.rank[j] += 1

        if self.rank[i] > self.rank[j]:
            i, j = j, i

        assert self.rank[i] < self.rank[j]
        self.parent[i] = j
        assert self.parent[j] < 0

        return True
