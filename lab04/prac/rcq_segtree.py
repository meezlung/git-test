""" Count How Many Times a Value v appears in the Range Query """
from collections.abc import Sequence
from typing import Generic, TypeVar

T = TypeVar("T")

class Node(Generic[T]):
    def __init__(self, seq: Sequence[T], i: int, j: int):
        self.i = i
        self.j = j

        if self.is_leaf():
            self.counts: dict[T, int] = {seq[i]: 1} # store freq count
            self.value = seq[i] # store the actual value
            self.l = self.r = None

        else:
            k = (i + j) // 2
            assert i < k < j

            self.l = Node(seq, i, k)
            self.r = Node(seq, k, j)
            self.combine()

    def is_leaf(self):
        return self.j - self.i == 1
    
    def get(self, i: int) -> T:
        if self.is_leaf():
            return self.value
        
        assert self.l is not None and self.r is not None

        if i < self.r.i:
            return self.l.get(i)
        else:
            return self.r.get(i)

    def set(self, i: int, v: T):
        if not self.i <= i < self.j:
            return
        
        if self.is_leaf():
            # update value
            old_value = self.value
            self.value = v

            # update freq count
            self.counts[old_value] = self.counts.get(old_value, 1) - 1
            if self.counts[old_value] == 0:
                del self.counts[old_value]
            self.counts[v] = self.counts.get(v, 0) + 1
        else:
            assert self.l is not None and self.r is not None
            self.l.set(i, v)
            self.r.set(i, v)
            self.combine()
            
    def combine(self):
        assert not self.is_leaf()
        assert self.l is not None and self.r is not None
        self.counts: dict[T, int] = {}
        for key in set(self.l.counts) | set(self.r.counts):
            self.counts[key] = self.l.counts.get(key, 0) + self.r.counts.get(key, 0)

    def count_range(self, i: int, j: int, v: T) -> int:
        if i <= self.i and self.j <= j:
            return self.counts.get(v, 0)
        elif j <= self.i or self.j <= i:
            return 0
        else:
            assert self.l is not None and self.r is not None
            return self.l.count_range(i, j, v) + self.r.count_range(i, j, v)
        

class RCQ(Generic[T]):
    def __init__(self, values: Sequence[T]):
        self.n = len(values)
        self.root = Node(values, 0, self.n)

    def __len__(self):
        return self.n

    def count_range(self, i: int, j: int, v: T) -> int:
        assert 0 <= i <= j <= self.n
        return self.root.count_range(i, j, v)

    def __setitem__(self, i: int, v: T):
        assert 0 <= i < self.n
        return self.root.set(i, v)
    
    def __getitem__(self, i: int):
        assert 0 <= i < self.n
        return self.root.get(i)


if __name__ == '__main__':
    values = [1, 2, 3, 2, 2, 3, 1, 4, 2, 3]
    rcq = RCQ(values)

    print(rcq.count_range(0, 10, 2))
    print(rcq[3])

    rcq[3] = 3

    print(rcq.count_range(0, 10, 2))
    print(rcq[3])