from __future__ import annotations
from collections import defaultdict
Edge = tuple[int, int]

class SegTree:
    def __init__(self, vals: list[int]) -> None:
        self.level: list[list[int]] = []
        self.leafs: int = 1 << (len(vals) - 1).bit_length()
        self.level_count: int = self.leafs.bit_length()

        self.null_val = 0
        for l in reversed(range(self.level_count)):
            self.level.append([self.null_val] * (1 << l))
        
        for idx, v in enumerate(vals):
            self.set(idx, v)
    
    def comb(self, a: int, b: int) -> int:
        return a + b

    def set(self, idx: int, val: int):
        self.level[0][idx] = val

        l = 1
        while l < self.level_count:
            up_idx = idx // 2
            up_val = self.comb(self.level[l-1][up_idx * 2], self.level[l-1][up_idx * 2 + 1])
            self.level[l][up_idx] = up_val
            
            l += 1
            idx = up_idx

    def _get(self, lvl: int, idx: int, i: int, j: int) -> int:
        ni = idx * (1 << lvl)
        nj =  (idx + 1) * (1 << lvl)

        if i <= ni and nj <= j: # if node fully between i and j
            return self.level[lvl][idx]
        elif j <= ni or nj <= i: # if node after j or node before i
            return self.null_val
        else:
            return self.comb(self._get(lvl-1, idx * 2, i, j),
                              self._get(lvl-1, idx * 2 + 1, i, j),)

    def get(self, i: int, j: int):
        assert i < j
        return self._get(self.level_count - 1, 0, i, j)
        

class TreeStruct:
    def __init__(self, edges: list[Edge], vals: list[int]) -> None:
        assert len(edges) + 1 == len(vals)

        self.root: int = edges[0][0]
        
        self.seg_idx: dict[int, int] = {}
        self.depth: dict[int, int] = {self.root: 0}
        self.parent: dict[int, int] = {self.root: self.root}
        self.top: dict[int, int] = {self.root: self.root}
        
        adj: defaultdict[int, list[int]] = defaultdict(list)
        for v1, v2 in edges:
            adj[v1].append(v2)
            adj[v2].append(v1)
        
        size: dict[int, int] = {}
        children: defaultdict[int, list[int]] = defaultdict(list)
        vis: set[int] = set()
        def dfs(node: int):
            vis.add(node)
            size[node] = 1

            for next in adj[node]:
                if next in vis:
                    continue
                self.depth[next] = self.depth[node] + 1
                self.parent[next] = node
                dfs(next)
                
                children[node].append(next)
                c_size = size[next]
                size[node] += c_size
                f_size = size[children[node][0]]
                if c_size > f_size:
                    children[node][0], children[node][-1] = (
                    children[node][-1], children[node][0]
                    )
        
        dfs(self.root)

        seq: list[int] = []
        def preorder(node: int):
            self.seg_idx[node] = len(seq)
            seq.append(node)
            for idx, child in enumerate(children[node]):
                self.top[child] = self.top[node] if idx == 0 else child
                preorder(child)
        
        preorder(self.root)
        
        self.segtree = SegTree(seq)

    def set(self, idx: int, val: int):
        self.segtree.set(self.seg_idx[idx], val)
    
    def get(self, node_1: int, node_2: int) -> int:
        ret = self.segtree.null_val
        depth = self.depth
        top = self.top
        seg_idx = self.seg_idx

        while (top[node_1] != top[node_2]):
            if depth[top[node_1]] < depth[top[node_2]]:
                node_1, node_2 = node_2, node_1
            
            #climb node 1
            s1, s2 = sorted((seg_idx[node_1], seg_idx[top[node_1]]))
            to_comb = self.segtree.get(s1, s2+1)
            ret = self.segtree.comb(to_comb, ret)
            node_1 = self.parent[top[node_1]]
        
        s1, s2 = sorted((seg_idx[node_1], seg_idx[node_2]))
        to_comb = self.segtree.get(s1, s2+1)
        ret = self.segtree.comb(to_comb, ret)

        return ret   
