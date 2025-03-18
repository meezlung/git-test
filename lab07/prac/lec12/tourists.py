# type: ignore
import sys, sys
import math
import heapq
from collections import defaultdict
from dataclasses import dataclass

sys.setrecursionlimit(300000)

#################################
# Bridges / 2ECC Preprocessing  #
#################################

@dataclass
class Edge:
    i: int
    j: int
    cost: int = 1

# Our DFS-based function to compute bridges (and BCCs) adapted to 1-indexed vertices.
def bridges_articulation_points_and_bccs(n: int, edges: list[Edge]):
    # Build adjacency list (1-indexed)
    adj = {i: [] for i in range(1, n+1)}
    for edge_idx, edge in enumerate(edges):
        adj[edge.i].append((edge.j, edge.cost, edge_idx, edge))
        adj[edge.j].append((edge.i, edge.cost, edge_idx, edge))
    
    # Check connectivity (we assume input graph is connected per problem statement)
    visited = set()
    def dfs_conn(u):
        stack = [u]
        while stack:
            cur = stack.pop()
            if cur not in visited:
                visited.add(cur)
                for v, *_ in adj[cur]:
                    stack.append(v)
    dfs_conn(1)
    if len(visited) != n:
        # Should not happen because graph is connected.
        return "NO", None

    low = [-1] * (n+1)
    vis = [-1] * (n+1)
    time = 0
    def visit(u):
        nonlocal time
        vis[u] = time
        time += 1

    bridges = []
    # We'll collect BCCs but for our DSU we only need bridges.
    edge_visited = [False] * len(edges)
    edge_stack = []
    bccs = []
    
    def extract_bcc(edge):
        comp = []
        while True:
            last_edge = edge_stack.pop()
            comp.append(last_edge)
            if last_edge == edge:
                break
        return comp

    def dfs(u, parent_edge):
        visit(u)
        low[u] = vis[u]
        children = 0
        for v, *_ , edge_idx, edge in adj[u]:
            if edge_visited[edge_idx]:
                continue
            edge_visited[edge_idx] = True
            if vis[v] == -1:
                edge_stack.append(edge)
                dfs(v, edge)
                low[u] = min(low[u], low[v])
                children += 1
                if low[v] > vis[u]:
                    bridges.append(edge)
                if low[v] >= vis[u]:
                    bccs.append(extract_bcc(edge))
            elif edge is not parent_edge:
                edge_stack.append(edge)
                low[u] = min(low[u], vis[v])
    dfs(1, None)
    return bridges, bccs

##########################
# DSU for 2ECC Extraction#
##########################

class DSU:
    def __init__(self, n):
        self.parent = list(range(n+1))
    def find(self, a):
        if self.parent[a] != a:
            self.parent[a] = self.find(self.parent[a])
        return self.parent[a]
    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            self.parent[b] = a

##############################
# Heavy Light Decomposition  #
##############################

class HLD:
    def __init__(self, tree, root=0):
        self.n = len(tree)
        self.tree = tree
        self.parent = [-1]*self.n
        self.depth = [0]*self.n
        self.size = [0]*self.n
        self.heavy = [-1]*self.n
        self.head = [0]*self.n
        self.pos = [0]*self.n
        self.cur_pos = 0
        self.dfs(root, -1)
        self.decompose(root, root)
        # Build segment tree on top of the array; initial values will be filled later.
        self.segsize = 1
        while self.segsize < self.n:
            self.segsize *= 2
        self.seg = [10**10]*(2*self.segsize)
    def dfs(self, u, p):
        self.parent[u] = p
        self.size[u] = 1
        max_size = 0
        for v in self.tree[u]:
            if v == p: continue
            self.depth[v] = self.depth[u] + 1
            self.dfs(v, u)
            if self.size[v] > max_size:
                max_size = self.size[v]
                self.heavy[u] = v
            self.size[u] += self.size[v]
    def decompose(self, u, h):
        self.head[u] = h
        self.pos[u] = self.cur_pos
        self.cur_pos += 1
        if self.heavy[u] != -1:
            self.decompose(self.heavy[u], h)
        for v in self.tree[u]:
            if v == self.parent[u] or v == self.heavy[u]:
                continue
            self.decompose(v, v)
    def seg_update(self, idx, value):
        # update value at position idx in segment tree
        i = idx + self.segsize
        self.seg[i] = value
        while i > 1:
            i //= 2
            self.seg[i] = min(self.seg[2*i], self.seg[2*i+1])
    def seg_query(self, l, r):
        # query [l, r]
        res = 10**10
        l += self.segsize
        r += self.segsize
        while l <= r:
            if (l % 2)==1:
                res = min(res, self.seg[l])
                l += 1
            if (r % 2)==0:
                res = min(res, self.seg[r])
                r -= 1
            l //= 2; r //= 2
        return res
    def query_path(self, u, v):
        res = 10**10
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] > self.depth[self.head[v]]:
                u, v = v, u
            res = min(res, self.seg_query(self.pos[self.head[v]], self.pos[v]))
            v = self.parent[self.head[v]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        res = min(res, self.seg_query(self.pos[u], self.pos[v]))
        return res

##############################################
# Main: Build Bridge Tree and Process Queries#
##############################################

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    q = int(next(it))
    city_price = [0]*(n+1)
    for i in range(1, n+1):
        city_price[i] = int(next(it))
    # Read roads
    orig_edges = []
    for _ in range(m):
        u = int(next(it)); v = int(next(it))
        orig_edges.append(Edge(u,v))
    
    # Compute bridges and BCCs on original graph.
    bridges, _ = bridges_articulation_points_and_bccs(n, orig_edges)
    bridge_set = set()
    for e in bridges:
        # Use tuple with ordered endpoints
        bridge_set.add((min(e.i, e.j), max(e.i, e.j)))
    
    # Build DSU by unioning all non-bridge edges.
    dsu = DSU(n)
    for e in orig_edges:
        if (min(e.i, e.j), max(e.i, e.j)) in bridge_set:
            continue
        dsu.union(e.i, e.j)
    # Map each vertex to its component
    comp_label = {}
    comp_of = [0]*(n+1)
    comp_list = defaultdict(list)
    comp_id = 0
    for i in range(1, n+1):
        rep = dsu.find(i)
        if rep not in comp_label:
            comp_label[rep] = comp_id
            comp_id += 1
        comp_of[i] = comp_label[rep]
        comp_list[comp_label[rep]].append(i)
    
    k = comp_id  # number of components
    # Build the bridge tree: nodes 0..k-1.
    tree = [[] for _ in range(k)]
    for e in bridges:
        u_comp = comp_of[e.i]
        v_comp = comp_of[e.j]
        if u_comp != v_comp:
            tree[u_comp].append(v_comp)
            tree[v_comp].append(u_comp)
    
    # For each component, maintain a min-heap of (price, city)
    comp_heap = {}
    comp_min = [10**10]*k
    for comp in range(k):
        comp_heap[comp] = []
        for city in comp_list[comp]:
            heapq.heappush(comp_heap[comp], (city_price[city], city))
        # Clean top if needed
        while comp_heap[comp] and comp_heap[comp][0][0] != city_price[comp_heap[comp][0][1]]:
            heapq.heappop(comp_heap[comp])
        if comp_heap[comp]:
            comp_min[comp] = comp_heap[comp][0][0]
    
    # Build HLD on the bridge tree.
    # If the tree is empty (i.e. k==1), then the whole graph is 2-edge-connected.
    hld = HLD(tree, 0) if k > 0 else None
    # Initialize segment tree with comp_min values.
    if hld:
        for comp in range(k):
            hld.seg_update(hld.pos[comp], comp_min[comp])
    
    output_lines = []
    # Process queries:
    for _ in range(q):
        typ = next(it)
        if typ == "C":
            a = int(next(it))
            w = int(next(it))
            # Update city a's price.
            city_price[a] = w
            comp = comp_of[a]
            # Push new price into the heap for component comp.
            heapq.heappush(comp_heap[comp], (w, a))
            # Lazy removal: pop outdated entries.
            while comp_heap[comp] and comp_heap[comp][0][0] != city_price[comp_heap[comp][0][1]]:
                heapq.heappop(comp_heap[comp])
            if comp_heap[comp]:
                new_min = comp_heap[comp][0][0]
            else:
                new_min = 10**10
            comp_min[comp] = new_min
            # Update HLD segment tree.
            if hld:
                hld.seg_update(hld.pos[comp], new_min)
        else:  # Query "A"
            a = int(next(it))
            b = int(next(it))
            comp_a = comp_of[a]
            comp_b = comp_of[b]
            if comp_a == comp_b:
                ans = comp_min[comp_a]
            else:
                # Query the HLD path from comp_a to comp_b.
                ans = hld.query_path(comp_a, comp_b)
            output_lines.append(str(ans))
    sys.stdout.write("\n".join(output_lines))
    
if __name__ == '__main__':
    main()
