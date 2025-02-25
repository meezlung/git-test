# type: ignore

from collections import defaultdict
from collections.abc import Sequence

class PartingWays:
    def __init__(self, roads: Sequence[tuple[int, int]]):
        self.n = len(roads) + 1
        self.graph = defaultdict(list)
        for a, b in roads:
            self.graph[a].append(b)
            self.graph[b].append(a)
        
        self.LOG = (self.n - 1).bit_length()
        self.depth = [0] * (self.n + 1)
        self.up = [[-1] * self.LOG for _ in range(self.n + 1)]
        self.precompute_lca(1, -1) 
    
    def precompute_lca(self, node: int, parent: int):
        self.up[node][0] = parent
        for i in range(1, self.LOG):
            if self.up[node][i - 1] != -1:
                self.up[node][i] = self.up[self.up[node][i - 1]][i - 1]
        
        for neighbor in self.graph[node]:
            if neighbor == parent:
                continue
            self.depth[neighbor] = self.depth[node] + 1
            self.precompute_lca(neighbor, node)
    
    def get_lca(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        
        diff = self.depth[u] - self.depth[v]
        for i in range(self.LOG):
            if (diff >> i) & 1:
                u = self.up[u][i]
        
        if u == v:
            return u
        
        for i in range(self.LOG - 1, -1, -1):
            if self.up[u][i] != self.up[v][i]:
                u = self.up[u][i]
                v = self.up[v][i]
        
        return self.up[u][0]
    
    def where_to_part(self, camp: int, rin: int, nadeshiko: int) -> int:
        lca_rin_root = self.get_lca(rin, camp)
        lca_nadeshiko_root = self.get_lca(nadeshiko, camp)
        lca_rin_nadeshiko = self.get_lca(rin, nadeshiko)
        
        return max(lca_rin_root, lca_nadeshiko_root, lca_rin_nadeshiko, key=lambda x: self.depth[x])
