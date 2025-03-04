from collections.abc import Sequence

class Node:
    def __init__(self, seq: Sequence[int], i: int, j: int):
        self.i = i
        self.j = j
        self.lazy = 0

        if self.is_leaf():
            self.sum_value = seq[i]
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

        self.sum_value = self.l.sum_value + self.r.sum_value

    def propagate(self):
        if self.lazy != 0:
            # apply pending update
            self.sum_value += (self.j - self.i) * self.lazy

            if not self.is_leaf():
                assert self.l is not None and self.r is not None
                # push update to children
                self.l.lazy += self.lazy
                self.r.lazy += self.lazy

            self.lazy = 0

    def range_sum_query(self, i: int, j: int) -> int:
        self.propagate()

        if i <= self.i and self.j <= j:
            return self.sum_value
        
        elif j <= self.i or self.j <= i:
            return 0
        
        else:
            assert self.l is not None and self.r is not None
            lsum = self.l.range_sum_query(i, j)
            rsum = self.r.range_sum_query(i, j)
            return lsum + rsum
        
    def range_update(self, i: int, j: int, v: int):
        # update coins from i to j
        self.propagate()

        if i <= self.i and self.j <= j:
            self.lazy += v # marked for lazy update
            self.propagate() 
            return
        
        elif j <= self.i or self.j <= i:
            return
        
        else:
            assert self.l is not None and self.r is not None
            self.l.range_update(i, j, v)
            self.r.range_update(i, j, v)
            self.combine()

class BowserTime:
    def __init__(self, initial_coins: Sequence[int]):
        self.n = len(initial_coins)
        self.root = Node(initial_coins, 0, self.n)
        super().__init__()

    def give_coins_to_range(self, l: int, r: int, x: int) -> None:
        # add x coins to coins[i - 1: j]
        self.root.range_update(l - 1, r, x)

    def give_coins_to_all_except(self, j: int, x: int) -> None:
        # add x coins to all coins except coins[j - 1]

        # update [0, j - 1)
        self.root.range_update(0, j - 1, x)

        # update (j, n)        
        self.root.range_update(j, self.n, x)

    def num_coins(self, j: int) -> int:
        # get coins[j - 1]
        return self.root.range_sum_query(j - 1, j)