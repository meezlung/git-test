""" Persistent RMQ """

from math import inf
from collections.abc import Sequence

class Node:
    def __init__(self, seq: Sequence[int], i: int, j: int,
                 l: "Node | None" = None, r: "Node | None" = None):
        self.i = i
        self.j = j

        if self.is_leaf():
            # leaf node
            self.min_value = seq[i]
            self.l = self.r = None

        else:
            # internal node
            self.l = l
            self.r = r
            self.combine()
    
    def is_leaf(self):
        return self.j - self.i == 1
    
    def combine(self):
        assert not self.is_leaf()
        assert self.l is not None and self.r is not None
        self.min_value = min(self.l.min_value, self.r.min_value)

    @staticmethod
    def build(seq: Sequence[int], i: int, j: int) -> "Node":
        if j - i == 1:
            return Node(seq, i, j)
        k = (i + j) // 2
        assert i < k < j

        l = Node.build(seq, i, k)
        r = Node.build(seq, k, j)
        return Node(seq, i, j, l, r)

    def get(self, i: int) -> int:
        if self.is_leaf():
            return self.min_value
        
        assert self.l is not None and self.r is not None

        if i < self.r.i:
            return self.l.get(i)
        else:
            return self.r.get(i)
        
    def set(self, i: int, v: int) -> "Node":
        if not self.i <= i < self.j:
            return self
        
        if self.is_leaf():
            # set the new min value
            return Node([v], self.i, self.j, None, None)

        assert self.l is not None and self.r is not None

        new_l = self.l.set(i, v) if i < self.r.i else self.l
        new_r = self.r.set(i, v) if i >= self.r.i else self.r

        return Node([0], self.i, self.j, new_l, new_r)

    def range_min(self, i: int, j: int) -> float:
        if i <= self.i and self.j <= j:
            return self.min_value
        elif j <= self.i or self.j <= i:
            return inf
        else:
            assert self.l is not None and self.r is not None

            lmin = self.l.range_min(i, j)
            rmin = self.r.range_min(i, j)
            return min(lmin, rmin)
        

class PersistentRMQ:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.root = Node.build(values, 0, self.n)

    def __len__(self):
        return self.n
    
    def range_min(self, i: int, j: int):
        assert 0 <= i <= j <= self.n
        return self.root.range_min(i, j)
    
    def update(self, i: int, v: int) -> "PersistentRMQ":
        assert 0 <= i < self.n
        new_rmq = PersistentRMQ.__new__(PersistentRMQ)
        new_rmq.n = self.n
        new_rmq.root = self.root.set(i, v)
        return new_rmq
    
    def __getitem__(self, i: int) -> int:
        assert 0 <= i < self.n
        return self.root.get(i)
    

if __name__ == '__main__':
    values = [1, 4, 5, 6, 3, 5, 6, 8, 2, 4]
    rmq = PersistentRMQ(values)

    print("Original RMQ:")
    print("Range min (4,7):", rmq.range_min(4, 7))
    print("Range min (0, len):", rmq.range_min(0, len(values)))
    print("Element 0:", rmq[0])

    # update returns a new RMQ instance
    rmq2 = rmq.update(0, 12)

    print("\nAfter update rmq[0] = 12 (new version):")
    print("New RMQ, element 0:", rmq2[0])
    print("New RMQ, range min (0, len):", rmq2.range_min(0, len(values)))

    # the original RMQ remains unchanged:
    print("\nOriginal RMQ remains unchanged:")
    print("Original element 0:", rmq[0])