from collections.abc import Sequence

class SegmentTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (4 * n)

    def _update(self, idx: int, val: int, node: int, start: int, end: int):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(idx, val, 2 * node + 1, start, mid)
        else:
            self._update(idx, val, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, idx: int, val: int):
        self._update(idx, val, 0, 0, self.n - 1)

    def _query(self, l: int, r: int, node: int, start: int, end: int) -> int:
        if r < start or l > end:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self._query(l, r, 2 * node + 1, start, mid) + \
               self._query(l, r, 2 * node + 2, mid + 1, end)

    def query(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return self._query(l, r, 0, 0, self.n - 1)


class TrapTracking:
    def __init__(self, connections: Sequence[tuple[int, int]]):
        self.n = 0
        for u, v in connections:
            self.n = max(self.n, u, v)
        self.adj: list[list[int]] = [[] for _ in range(self.n + 1)]
        for u, v in connections:
            self.adj[u].append(v)
            self.adj[v].append(u)

        self.parent = [-1] * (self.n + 1)
        self.depth  = [0]  * (self.n + 1)
        self.size   = [0]  * (self.n + 1)
        self.heavy  = [-1] * (self.n + 1)  # heavy child
        self.head   = [0]  * (self.n + 1)  # head of chain
        self.pos    = [0]  * (self.n + 1)  # position in base array
        self.cur_pos = 0
        self.traps   = [False] * (self.n + 1)  # track if node is trapped

        self._dfs(1, -1, 0)  # root at node 1
        self._decompose(1, 1)

        self.base = [0] * self.n
        # root node has no parent edge

        self.seg = SegmentTree(self.n)

    def _dfs(self, u: int, p: int, d: int):
        self.parent[u] = p
        self.depth[u] = d
        self.size[u] = 1

        max_sub = -1
        for c in self.adj[u]:
            if c == p: 
                continue
            self._dfs(c, u, d + 1)
            if self.size[c] > max_sub:
                max_sub = self.size[c]
                self.heavy[u] = c
            self.size[u] += self.size[c]

    def _decompose(self, u: int, h: int):
        self.head[u] = h
        self.pos[u] = self.cur_pos
        self.cur_pos += 1

        # decompose heavy child first
        if self.heavy[u] != -1:
            self._decompose(self.heavy[u], h)

        # decompose light children
        for c in self.adj[u]:
            if c == self.parent[u] or c == self.heavy[u]:
                continue
            self._decompose(c, c)

    def _update_edge(self, node: int):
        p = self.parent[node]
        if p == -1:  # root
            return
        val = 1 if (self.traps[node] and self.traps[p]) else 0
        idx = self.pos[node]
        self.base[idx] = val
        self.seg.update(idx, val)

    def place_trap(self, a: int):
        if self.traps[a]:
            return  # already trapped
        self.traps[a] = True

        # update edge (a->parent[a])
        self._update_edge(a)

        # also each child c where parent[c] = a
        # we can find them by checking heavy decomposition or adjacency
        for c in self.adj[a]:
            if self.parent[c] == a:  # c is child
                self._update_edge(c)

    def remove_trap(self, a: int):
        if not self.traps[a]:
            return
        self.traps[a] = False

        self._update_edge(a)

        for c in self.adj[a]:
            if self.parent[c] == a:
                self._update_edge(c)

    def _path_query(self, u: int, v: int) -> int:
        s = 0
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] > self.depth[self.head[v]]:
                u, v = v, u
            # now v is deeper chain
            # sum segment [pos[head[v]]..pos[v]]
            topv = self.head[v]
            s += self.seg.query(self.pos[topv], self.pos[v])
            v = self.parent[topv]
        # same chain now
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        # sum [pos[u]+1..pos[v]] => edges from (u->parent[u]) not included if u is root
        # but we want edges in the path from u..v, so skip pos[u] itself
        s += self.seg.query(self.pos[u] + 1, self.pos[v])
        return s

    def num_trappy(self, a: int, b: int) -> int:
        return self._path_query(a, b)
