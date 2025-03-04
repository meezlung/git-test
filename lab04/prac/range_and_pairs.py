from collections.abc import Sequence

class Node:
    def __init__(self, seq: Sequence[int], i: int, j: int):
        self.i = i
        self.j = j
        if self.is_leaf():
            self.trap_sum = seq[i]
            self.pair_count = 0  # No pairs in a leaf
            self.left_value = seq[i]  # Value at the left end of the interval
            self.right_value = seq[i]  # Value at the right end of the interval
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
        
        # Combine trap sums
        self.trap_sum = self.l.trap_sum + self.r.trap_sum
        
        # Combine pair counts
        self.pair_count = self.l.pair_count + self.r.pair_count
        
        # Check if the right value of the left child and the left value of the right child form a pair
        if self.l.right_value == 1 and self.r.left_value == 1:
            self.pair_count += 1
        
        # Update left and right values
        self.left_value = self.l.left_value
        self.right_value = self.r.right_value

    def get(self, i: int) -> int:
        if self.is_leaf():
            return self.trap_sum
        assert self.l is not None and self.r is not None
        if i < self.r.i:
            return self.l.get(i)
        else:
            return self.r.get(i)

    def set(self, i: int, v: int):
        if not self.i <= i < self.j:
            return
        if self.is_leaf():
            self.trap_sum = v
            self.left_value = v
            self.right_value = v
        else:
            assert self.l is not None and self.r is not None
            self.l.set(i, v)
            self.r.set(i, v)
            self.combine()

    def range_trap_pairs(self, i: int, j: int) -> int:
        if i <= self.i and self.j <= j:
            return self.pair_count
        elif j <= self.i or self.j <= i:
            return 0
        else:
            assert self.l is not None and self.r is not None
            return self.l.range_trap_pairs(i, j) + self.r.range_trap_pairs(i, j)


class RAQ:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.root = Node(values, 0, self.n)

    def __len__(self):
        return self.n

    def range_trap_pairs(self, i: int, j: int):
        assert 0 <= i <= j <= self.n
        return self.root.range_trap_pairs(i, j)

    def __setitem__(self, i: int, v: int) -> None:
        assert 0 <= i < self.n
        self.root.set(i, v)


if __name__ == '__main__':
    values = [1, 1, 1, 1, 1, 1, 1, 1]
    raq = RAQ(values)
    print(raq.range_trap_pairs(0, 8))  # Output: 0 (no consecutive pairs of 1s)