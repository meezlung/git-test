# type: ignore
from collections import defaultdict, deque

class Investigation:
    def __init__(self, n: int, connections):
        self.n = n
        # Build undirected graph (1-indexed)
        self.graph = [[] for _ in range(n+1)]
        for u, v in connections:
            self.graph[u].append(v)
            self.graph[v].append(u)
        # Tarjan DFS to get articulation points and biconnected components.
        self._tarjan()
        # Build the block–cut tree and record a representative for each spot.
        self._build_BC_tree()
        # Precompute LCA on the BC–tree.
        self._precompute_LCA()

    def _tarjan(self):
        n = self.n
        self.disc = [0]*(n+1)
        self.low = [0]*(n+1)
        self.time = 1
        self.art = [False]*(n+1)
        self.bcc = []  # list of bcc's, each is a list of vertices
        self.stack = []
        # We'll store bcc membership for non-articulation vertices later.
        def dfs(u, parent):
            self.disc[u] = self.low[u] = self.time
            self.time += 1
            child_count = 0
            for v in self.graph[u]:
                if v == parent:
                    continue
                if not self.disc[v]:
                    self.stack.append( (u,v) )
                    child_count += 1
                    dfs(v, u)
                    self.low[u] = min(self.low[u], self.low[v])
                    if (parent != -1 and self.low[v] >= self.disc[u]) or (parent == -1 and child_count > 1):
                        self.art[u] = True
                        # pop edges to form a BCC
                        comp = set()
                        while self.stack:
                            e = self.stack.pop()
                            comp.add(e[0])
                            comp.add(e[1])
                            if e == (u,v):
                                break
                        self.bcc.append(comp)
                elif self.disc[v] < self.disc[u]:
                    self.stack.append( (u,v) )
                    self.low[u] = min(self.low[u], self.disc[v])
        for i in range(1, n+1):
            if not self.disc[i]:
                dfs(i, -1)
                if self.stack:
                    comp = set()
                    while self.stack:
                        e = self.stack.pop()
                        comp.add(e[0])
                        comp.add(e[1])
                    self.bcc.append(comp)
        # Now, self.art[v] is True if v is an articulation point.
        # For convenience, let self.is_art[v] be a boolean.
        self.is_art = self.art

    def _build_BC_tree(self):
        n = self.n
        # In the BC-tree, we will have two types of nodes:
        #  - Articulation nodes: use their original label (1..n) for each v with self.is_art[v]==True.
        #  - BCC nodes: assign new ids starting from n+1.
        self.T = defaultdict(list)  # BC-tree (undirected)
        self.rep = [None]*(n+1)     # rep[v]: the BC-tree node representing v
        bcc_id = n
        # For each bcc component, add a node.
        # Also record for non-articulation vertices: they appear in exactly one bcc.
        # For articulation vertices, they may appear in many, but we represent them by themselves.
        for comp in self.bcc:
            bcc_id += 1
            # For every vertex in comp:
            for v in comp:
                if self.is_art[v]:
                    # add edge between v and this bcc node
                    self.T[v].append(bcc_id)
                    self.T[bcc_id].append(v)
                else:
                    # non-articulation: it appears in exactly one bcc.
                    # If already assigned, do nothing.
                    if self.rep[v] is None:
                        self.rep[v] = bcc_id
            # (Note: even if an articulation point v appears in comp, its rep is v.)
        # For every vertex that is an articulation point, set rep[v] = v.
        for v in range(1, n+1):
            if self.is_art[v]:
                self.rep[v] = v
            # In a connected graph, every vertex gets a rep.
        # Save the number of nodes in the tree.
        self.T_nodes = set(self.T.keys())
        # Record f: f(x)=1 if x is an articulation node (i.e. x<=n) else 0.
        max_node = max(self.T_nodes) if self.T_nodes else 0
        self.f = [0]*(max_node+1)
        for x in self.T_nodes:
            if x <= n and self.is_art[x]:
                self.f[x] = 1
            else:
                self.f[x] = 0

    def _precompute_LCA(self):
        # Precompute LCA (and path–sum) on the BC–tree.
        # The tree T has nodes in self.T_nodes. We choose an arbitrary root.
        if not self.T_nodes:
            return
        # Choose root as rep(1)
        root = self.rep[1]
        max_node = max(self.T_nodes)
        N = max_node + 1
        self.depth = [-1]*N
        self.parent0 = [-1]*N  # immediate parent in DFS tree
        self.psum = [0]*N    # prefix sum of f-values along tree (including self)
        # DFS (or BFS) on the tree T
        dq = deque()
        self.depth[root] = 0
        self.parent0[root] = -1
        self.psum[root] = self.f[root]
        dq.append(root)
        while dq:
            u = dq.popleft()
            for v in self.T[u]:
                if self.depth[v] == -1:
                    self.depth[v] = self.depth[u] + 1
                    self.parent0[v] = u
                    self.psum[v] = self.psum[u] + self.f[v]
                    dq.append(v)
        # Build binary lifting table.
        # Let L = floor(log2(N)) + 1.
        L = (max_node+1).bit_length()
        self.dp = [ [-1]*N for _ in range(L) ]
        for i in range(N):
            self.dp[0][i] = self.parent0[i]
        for k in range(1, L):
            for i in range(N):
                par = self.dp[k-1][i]
                self.dp[k][i] = self.dp[k-1][par] if par != -1 else -1
        self.L = L

    def _lca(self, u: int, v: int) -> int:
        # Assume u and v are nodes in the BC–tree (their ids are < len(self.depth))
        if u == -1 or v == -1:
            return -1
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        # Lift u up so that depth[u] == depth[v]
        d = self.depth[u] - self.depth[v]
        k = 0
        while d:
            if d & 1:
                u = self.dp[k][u]
            d //= 2
            k += 1
        if u == v:
            return u
        for k in range(self.L-1, -1, -1):
            if self.dp[k][u] != self.dp[k][v]:
                u = self.dp[k][u]
                v = self.dp[k][v]
        return self.parent0[u]

    def _path_sum(self, u: int, v: int) -> int:
        # Return the sum of f-values on the unique path from u to v in the tree.
        l = self._lca(u, v)
        if l == -1:
            return 0
        return self.psum[u] + self.psum[v] - 2*self.psum[l] + self.f[l]

    def min_shared_spots(self, a: int, b: int) -> int:
        # If a==b, no travel occurs so answer is 0.
        if a == b:
            return 0
        u = self.rep[a]
        v = self.rep[b]
        # The BC–tree path from u to v has sum = (number of unavoidable (articulation) nodes).
        tot = self._path_sum(u, v)
        # But if a (or b) itself is an articulation point, it is counted in tot;
        # we are told not to count spots a and b.
        if self.is_art[a]:
            tot -= 1
        if self.is_art[b]:
            tot -= 1
        return tot