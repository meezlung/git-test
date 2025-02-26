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
            self.l.set(i, v)
            self.r.set(i, v)
            self.combine()

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
        
    def inc_range(self, i: int, j: int):
        for x in range(i, j):
            self.set(x, self.get(x) + 1)
    

class RMQ:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.root = Node(values, 0, self.n)

    def __len__(self):
        return self.n
    
    def range_query(self, i: int, j: int):
        assert 0 <= i <= j <= self.n
        return self.root.range_min(i, j)

    def __getitem__(self, i: int):
        assert 0 <= i < self.n
        return self.root.get(i)
    
    def __setitem__(self, i: int, v: int):
        assert 0 <= i < self.n
        self.root.set(i, v)

    def inc_range(self, i: int, j: int):
        assert 0 <= i <= j <= self.n
        self.root.inc_range(i, j)


if __name__ == "__main__":
    values = [3, 1, 4, 1, 5, 1, 9]
    
    rmq = RMQ(values)

    print(rmq[0])
    print(rmq.range_query(0, 7))

    rmq[0] = 0

    print(rmq[0])
    print(rmq.range_query(0, 7))
    
    rmq.inc_range(0, 7)

    print(rmq.range_query(0, 7))

    for i in range(7):
        print("bruh")
        print(rmq[i])
