""" Range Parenthesis Query """
from collections.abc import Sequence

class Node:
    def __init__(self, seq: Sequence[str], i: int, j: int):
        self.i = i
        self.j = j

        if i == -1 and j == -1:
            self.open = self.close = self.min_bal = 0
            self.l = self.r = self

        elif self.is_leaf():
            self.open: int = 1 if seq[i] == '(' else 0
            self.close: int = 1 if seq[i] == ')' else 0
            self.min_bal = self.open - self.close
            self.l = self.r = None

        else: 
            k = (i + j) // 2
            assert i < k < j

            # [i, j] = [i, k) + [k, j)
            self.l = Node(seq, i, k)
            self.r = Node(seq, k, j)
            self.combine()

    def is_leaf(self):
        return self.j - self.i == 1
    
    def combine(self):
        if self.l is None or self.r is None:  # Identity nodes should NOT be combined!
            return

        matched = min(self.l.open, self.r.close)

        self.open = self.l.open + self.r.open - matched
        self.close = self.l.close + self.r.close - matched

        total_balance = self.l.open - self.l.close
        self.min_bal = min(self.l.min_bal, total_balance + self.r.min_bal)

    def range_query(self, i: int, j: int) -> "Node | None":
        if i <= self.i and self.j <= j:
            # completely contained
            return self 
        elif j <= self.i or self.j <= i:
            # completely nonoverlapping
            return Node.identity()
        else:
            assert self.l is not None and self.r is not None
            left = self.l.range_query(i, j)
            right = self.r.range_query(i, j)

            if left is None:
                return right
            if right is None:
                return left

            new_node = Node.identity()
            new_node.i = i
            new_node.j = j
            new_node.l = left
            new_node.r = right
            new_node.combine()
            return new_node
        
    @staticmethod
    def identity():
        node = Node([], -1, -1)
        node.open = node.close = node.min_bal = 0
        node.l = node.r = None
        return node

class RPQ:
    def __init__(self, seq: str):
        self.values = seq
        self.n = len(self.values)
        self.root = Node(self.values, 0, self.n)

    def range_max_seq(self, i: int, j: int) -> int:
        node = self.root.range_query(i, j)
        if node is None:
            return 0
        return (j - i) - (node.open + node.close) # guaranteed this is matched pair
    
if __name__ == '__main__':
    import sys

    bracket_seq = sys.stdin.readline().strip()
    q = int(sys.stdin.readline())

    queries: list[tuple[int, int]] = []

    for _ in range(q):
        i, j = map(int, sys.stdin.readline().split())
        queries.append((i, j))
        
    print(bracket_seq)

    rpq = RPQ(bracket_seq)

    for i, j in queries:
        print(f"{i, j}: {rpq.range_max_seq(i - 1, j)}")