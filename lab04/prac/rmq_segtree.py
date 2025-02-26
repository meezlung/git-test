""" Range Minimum Query """

from collections.abc import Sequence
from math import inf

class Node:
    def __init__(self, seq: Sequence[int], i: int, j: int):
        self.i = i
        self.j = j

        if self.is_leaf():
            self.min_value = seq[i]
            self.l = self.r = None

        else:
            k = (i + j) // 2
            assert i < k < j

            # [i, j) = [i, k) + [k, j)
            self.l = Node(seq, i, k)
            self.r = Node(seq, k, j)
            self.combine()

    def is_leaf(self):
        return self.j - self.i == 1

    def combine(self):
        assert not self.is_leaf()
        assert self.l is not None and self.r is not None
        self.min_value = min(self.l.min_value, self.r.min_value)

    def get(self, i: int) -> int:
        if self.is_leaf():
            return self.min_value
        
        assert self.l is not None and self.r is not None

        if i < self.r.i:
            return self.l.get(i)
        else:
            return self.r.get(i)

    def set(self, i: int, v: int):
        if not self.i <= i < self.j:
            return
        
        if self.is_leaf():
            self.min_value = v
        
        else:
            assert self.l is not None and self.r is not None

            # only 1 will run here because of our base case.
            self.l.set(i, v)
            self.r.set(i, v)

            self.combine() # update the value to this node

    def range_min(self, i: int, j: int) -> int | float:
        # i, j are indices
        if i <= self.i and self.j <= j:
            # completely contained
            return self.min_value
    
        elif j <= self.i or self.j <= i:
            # completely non-overlapping
            return inf
        
        else:
            assert self.l is not None and self.r is not None
            # partial overlap
            lmin = self.l.range_min(i, j)
            rmin = self.r.range_min(i, j)
            return min(lmin, rmin)
        

class RMQ:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.root = Node(values, 0, self.n)

    def __len__(self):
        return self.n
    
    def range_min(self, i: int, j: int):
        assert 0 <= i <= j <= self.n
        if i > j:
            i, j = j, i
        return self.root.range_min(i, j)
    
    def __setitem__(self, i: int, v: int) -> None:
        assert 0 <= i < self.n
        self.root.set(i, v)

    def __getitem__(self, i: int) -> int:
        assert 0 <= i < self.n
        return self.root.get(i)


if __name__ == '__main__':
    values = [1, 4, 5, 6, 3, 5, 6, 8, 2, 4]
    rmq = RMQ(values)
    print(rmq.range_min(4, 7))
    print(rmq.range_min(0, len(values)))
    print(rmq[0])
    rmq[0] = 12
    print(rmq[0])