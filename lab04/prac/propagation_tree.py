""" Lazy Propagation """
from collections.abc import Sequence

class Node:
    def __init__(self, seq: Sequence[int], i: int, j: int):
        self.i = i
        self.j = j
        self.lazy = 0

        if self.is_leaf():
            self.value = seq[i]
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
        self.value = self.l.value + self.r.value

    def propagate(self):
        """ push lazy updates to child nodes if necessary """
        if self.lazy != 0 and not self.is_leaf():
            assert self.l is not None and self.r is not None
            self.l.lazy += self.lazy
            self.r.lazy += self.lazy
            self.l.value += self.lazy * (self.l.j - self.l.i)
            self.r.value += self.lazy * (self.r.j - self.r.i)
            self.lazy = 0

    def update_range(self, i: int, j: int, v: int):
        self.propagate()

        if i <= self.i and self.j <= j:
            self.value += v * (self.j - self.i)
            self.lazy += v
            return
    
        if j <= self.i or self.j <= i:
            return
        
        assert self.l is not None and self.r is not None
        self.l.update_range(i, j, v)
        self.r.update_range(i, j, v)
        self.combine()

    def get(self, i: int) -> int:
        self.propagate()

        if self.is_leaf():
            return self.value
        
        assert self.l is not None and self.r is not None

        if i < self.r.i:
            return self.l.get(i)
        else:
            return self.r.get(i)
        
    
class SMQ:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.root = Node(values, 0, self.n)

    def __len__(self):
        return self.n

    def add_range(self, i: int, j: int, v: int):
        assert 0 <= i <= j <= self.n
        self.root.update_range(i, j, v)

    def __getitem__(self, i: int):
        assert 0 <= i < self.n
        return self.root.get(i)
    
import sys

n, m = map(int, sys.stdin.readline().split())
seq = list(map(int, sys.stdin.readline().split()))

adj: dict[int, list[int]] = {i: [] for i in range(n + 1)}

for _ in range(n - 1):
    v, u = map(int, sys.stdin.readline().split())
    adj[v].append(u)
    adj[u].append(v)

# euler tour

start = [0] * (n + 1)
end = [0] * (n + 1)
euler = [0] * (n + 1)
timer = [0]

def dfs(node: int, parent: int, adj: dict[int, list[int]], euler: list[int], start: list[int], end: list[int], timer: list[int]):
    start[node] = timer[0]
    euler[timer[0]] = node
    timer[0] += 1

    for child in adj[node]:
        if child != parent:
            dfs(child, node, adj, euler, start, end, timer)
    
    end[node] = timer[0]

dfs(1, -1, adj, euler, start, end, timer)

# initialize segment tree    
values = [0] * n
for i in range(1, n + 1):
    values[start[i]] = seq[i - 1]
segment_tree = SMQ(values)

# set init values
for i in range(n):
    segment_tree.add_range(start[i + 1], start[i + 1] + 1, seq[i])

output: list[str] = []

# process queries
for _ in range(m):
    query = tuple(map(int, sys.stdin.readline().split()))

    if query[0] == 1:
        x = query[1]
        val = query[2]

        segment_tree.add_range(start[x], end[x], val)

    else:
        x = query[1]

        output.append(str(segment_tree[start[x]]))

for o in output:
    print(o)