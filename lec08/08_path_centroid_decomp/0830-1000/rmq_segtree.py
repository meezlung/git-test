# type: ignore

from collections.abc import Sequence
from math import inf


class Node:
    # i: int
    # j: int
    # min_value: int
    # l: "Node | None" = None
    # r: "Node | None" = None
    def __init__(self, seq: Sequence[int], i: int, j: int):
        # This node represents the half-open interval [i, j)
        self.i = i
        self.j = j
        if self.is_leaf():
            self.min_value = seq[i]
            self.l = self.r = None
        else:
            # split interval into roughly half
            k = (i + j) // 2
            assert i < k < j
            # note that [i, j) = [i, k) + [k, j)
            self.l = Node(seq, i, k)
            self.r = Node(seq, k, j)
            self.combine()

        super().__init__()


    def is_leaf(self):
        return self.j - self.i == 1


    def combine(self):
        # compute new minimum
        assert not self.is_leaf()
        self.min_value = min(self.l.min_value, self.r.min_value)


    def set(self, i, v):
        if not self.i <= i < self.j:
            # index i not in this node, we can skip
            return

        if self.is_leaf():
            self.min_value = v
        else:
            self.l.set(i, v)
            self.r.set(i, v)
            self.combine()


    def range_min(self, i, j):
        if i <= self.i and self.j <= j:
            # completely contained
            return self.min_value
        elif j <= self.i or self.j <= i:
            # completely non-overlapping
            return inf
        else:
            # partial overlap
            lmin = self.l.range_min(i, j)
            rmin = self.r.range_min(i, j)
            return min(lmin, rmin)


class RMQ:
    def __init__(self, values: Sequence[int]):
        self._len = len(values)
        self.root = Node(values, 0, len(values))
        super().__init__()


    def __len__(self) -> int:
        return self._len


    def range_min(self, i: int, j: int):
        assert 0 <= i <= j <= len(self)
        return self.root.range_min(i, j)


    def __setitem__(self, i: int, v: int) -> None:
        assert 0 <= i < len(self)
        self.root.set(i, v)
