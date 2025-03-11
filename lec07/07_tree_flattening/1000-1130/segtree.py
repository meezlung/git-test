# type: ignore

class Node:
    def __init__(self, seq, i, j):
        # [i, j)
        self.i = i
        self.j = j
        if self.is_leaf():
            self.v = seq[i]
            self.l = self.r = None
        else:
            m = (i + j) // 2
            self.l = Node(seq, i, m)
            self.r = Node(seq, m, j)
            self.combine()
        super().__init__()

    def combine(self):
        self.v = self.l.v + self.r.v

    def sum(self, i, j):
        if i <= self.i and self.j <= j:
            return self.v
        elif j <= self.i or i >= self.j:
            return 0
        else:
            return self.l.sum(i, j) + self.r.sum(i, j)

    def set(self, i, v):
        if self.i <= i < self.j:
            if self.is_leaf():
                self.v = v
            else:
                self.l.set(i, v)
                self.r.set(i, v)
                self.combine()

    def is_leaf(self):
        return self.i + 1 == self.j


class RangeSums:
    def __init__(self, seq):
        self.root = Node(seq, 0, len(seq))
        self.seq = seq
        super().__init__()

    def sum(self, i, j):
        return self.root.sum(i, j)

    def set(self, i, v):
        self.root.set(i, v)
        self.seq[i] = v


if __name__ == '__main__':
    li = [5, 3, 1, 7, 4, 8]  # , 6, 2]
    rsq = RangeSums(li)  # segment tree for range sum query
    print(rsq.seq)

    queries = [(0, 3), (2, 3), (1, 5), (0, 6), (2, 6), (4, 6)]
    for l, r in queries:
        print(f'sum in [{l}, {r}) is {rsq.sum(l, r)}')

    print('setting some values...')
    rsq.set(3, 6)
    rsq.set(1, 2)
    rsq.set(4, 5)
    rsq.set(5, 11)

    print(rsq.seq)

    for l, r in queries:
        print(f'sum in [{l}, {r}) is {rsq.sum(l, r)}')

    # print(rsq.sum(2, 2))