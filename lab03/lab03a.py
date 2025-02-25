# type: ignore

from collections.abc import Sequence
from collections import defaultdict

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 2 ** (self.n - 1).bit_length()
        self.tree = [0] * (2 * self.size)
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def query(self, l, r):
        res = 0
        l += self.size
        r += self.size + 1
        while l < r:
            if l % 2 == 1:
                res += self.tree[l]
                l += 1
            if r % 2 == 1:
                r -= 1
                res += self.tree[r]
            l //= 2
            r //= 2
        return res

class FoodTrip:
    def __init__(self, roads: Sequence[tuple[int, int]], costs: Sequence[int]):
        self.n = len(costs)
        self.costs = costs
        self.graph = defaultdict(list)
        for a, b in roads:
            self.graph[a].append(b)
            self.graph[b].append(a)
        
        self.parent = [0] * (self.n + 1)
        self.depth = [0] * (self.n + 1)
        self.heavy = [-1] * (self.n + 1)
        self.head = [0] * (self.n + 1)
        self.pos = [0] * (self.n + 1)
        self.cur_pos = 0

        self.dfs(1)
        self.decompose(1, 1)
        self.segment_trees = {}
        self.build_segment_trees()

    def dfs(self, node):
        size = 1
        max_size = 0
        for child in self.graph[node]:
            if child != self.parent[node]:
                self.parent[child] = node
                self.depth[child] = self.depth[node] + 1
                child_size = self.dfs(child)
                size += child_size
                if child_size > max_size:
                    max_size = child_size
                    self.heavy[node] = child
        return size

    def decompose(self, node, h):
        self.head[node] = h
        self.pos[node] = self.cur_pos
        self.cur_pos += 1
        if self.heavy[node] != -1:
            self.decompose(self.heavy[node], h)
        for child in self.graph[node]:
            if child != self.parent[node] and child != self.heavy[node]:
                self.decompose(child, child)

    def build_segment_trees(self):
        data = [0] * self.n
        for i in range(1, self.n + 1):
            data[self.pos[i]] = self.costs[i - 1]
        self.segment_trees[1] = SegmentTree(data)

    def path_sum(self, u, v):
        res = 0
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            res += self.segment_trees[1].query(self.pos[self.head[u]], self.pos[u])
            u = self.parent[self.head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        res += self.segment_trees[1].query(self.pos[u], self.pos[v])
        return res

    def money_needed(self, start: int, end: int) -> int:
        return self.path_sum(start, end)