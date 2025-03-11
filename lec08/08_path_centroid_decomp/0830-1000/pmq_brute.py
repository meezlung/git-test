# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import product
from math import inf

from utils import Edge


class PMQ:
    def __init__(self, values: Sequence[int], edges: Sequence[Edge]):
        self.n = len(values)

        self.values = [*values]
        self.edges = edges
        self.compute_everything()
        super().__init__()


    def compute_everything(self):
        # mn[i][j] = minimum from i to j

        shp = [[0 if i == j else self.n for j in range(self.n)] for i in range(self.n)]
        for edge in self.edges:
            shp[edge.i][edge.j] = shp[edge.j][edge.i] = 1

        # Floyd
        for k, i, j in product(range(self.n), repeat=3):
            shp[i][j] = min(shp[i][j], shp[i][k] + shp[k][j])

        self.mn = [[inf]*self.n for i in range(self.n)]

        def min_path(i, j):
            if shp[i][j] <= 1:
                return min(self.values[i], self.values[j])
            else:
                k = next(k for k in range(self.n) if shp[i][j] == shp[i][k] + shp[k][j] and k not in {i, j})
                return min(min_path(i, k), min_path(k, j))

        for i in range(self.n):
            for j in range(self.n):
                self.mn[i][j] = min_path(i, j)


    def __len__(self):
        return self.n


    def path_min(self, i: int, j: int):
        """min of values in the path from i to j"""
        assert all(0 <= k < len(self) for k in (i, j))
        return self.mn[i][j]


    def __setitem__(self, i: int, v: int) -> None:
        """set the value at i to v"""
        assert 0 <= i < len(self)
        self.values[i] = v
        self.compute_everything()


def offline_pmq(values: Sequence[int], edges: Sequence[Edge], queries: Sequence[tuple[int, int]]):
    # we can solve offline RMQ online
    pmq = PMQ(values, edges)
    return [pmq.path_min(i, j) for i, j in queries]
