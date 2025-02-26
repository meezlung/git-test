""" Find First Greater between a Range Query """
from collections.abc import Sequence

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

    def find_first_greater(self, i: int, j: int, v: int) -> int:
        if self.is_leaf():
            return self.i if self.min_value > v else -1
        
        if j <= self.i or self.j <= i:
            return -1 # out of range
        
        # if self.min_value <= v:
        #     return -1 # no valid answer
        
        assert self.l is not None and self.r is not None
        
        left_result = self.l.find_first_greater(i, j, v)
        if left_result != -1:
            return left_result
        return self.r.find_first_greater(i, j, v)


class RFFG:
    def __init__(self, seq: Sequence[int]):
        self.n = len(seq)
        self.root = Node(seq, 0, self.n)

    def __len__(self):
        return self.n
    
    def find_first_greater(self, i: int, j: int, v: int):
        assert 0 <= i <= j <= self.n
        return self.root.find_first_greater(i, j, v)
    
    def __setitem__(self, i: int, v: int):
        assert 0 <= i < self.n
        return self.root.set(i, v)
    
    def __getitem__(self, i: int):
        assert 0 <= i < self.n
        return self.root.get(i)
    

if __name__ == '__main__':
    values = [1, 4, 5, 6, 3, 5, 6, 8, 2, 4]
    rffg = RFFG(values)

    print(rffg.find_first_greater(0, 10, 4))
    print(rffg[1])
    rffg[1] = 10
    print(rffg.find_first_greater(0, 10, 4))
    print(rffg[1])
