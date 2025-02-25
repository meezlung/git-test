    
import sys
from dataclasses import dataclass, field
from collections.abc import Sequence
from collections import deque

@dataclass
class Node:
    label: int
    parent: "Node | None" = None
    depth: int = 0
    children: "list[Node]" = field(default_factory=list)
    jump: "list[Node]" = field(default_factory=list)

class RootedTree:
    def __init__(self, parent: Sequence[int], _root: int):
        n = len(parent)
        assert 0 <= _root < n

        # setup nodes
        self.nodes = [Node(i) for i in range(n)]

        # setup root
        self.root = root = self.nodes[_root]

        # setup parent
        for i in range(n):
            self.nodes[i].parent = self.nodes[parent[i]]

            if parent[i] != i:
                self.nodes[parent[i]].children.append(self.nodes[i])

        # assert root.parent is root

        # dfs from and update depth along the way
        def dfs(i: Node):
            for j in i.children:
                j.depth = i.depth + 1
                dfs(j)

        dfs(root)

        # initialize height
        self.h = h = n.bit_length()

        # initialize powers-of-two pointers
        for i in self.nodes:
            assert i.parent is not None
            i.jump = [i]*h # all can jump to itself muna
            i.jump[0] = i.parent # point the first as the parent obv

        # the amazing dp 
        for k in range(h - 1):
            for i in self.nodes:
                i.jump[k + 1] = i.jump[k].jump[k]

    
    def climb(self, i: Node, d: int):
        for k in reversed(range(self.h)):
            if i.depth >= d + (1 << k): # if mas mababa ung i, jump higher
                i = i.jump[k]

        assert i.depth <= d
        return i


    def _lca(self, i: Node | None, j: Node | None):
        if i is None or j is None:
            return None
        
        i = self.climb(i, j.depth)
        j = self.climb(j, i.depth)

        # assume na same level na sila
        assert i.depth == j.depth

        # pagsabay na galaw
        for k in reversed(range(self.h)):
            if i.jump[k] is not j.jump[k]:
                i = i.jump[k]
                j = j.jump[k]

        if i is not j:
            i = i.parent
            j = j.parent

        assert i is j
        return i
        

    def lca(self, i: int, j: int):
        lca = self._lca(self.nodes[i], self.nodes[j])
        return lca.label if lca else None

n = int(sys.stdin.readline().strip())

# tree structure
edges: list[tuple[int, int]] = []
adj_list: list[list[int]] = [[] for _ in range(n)]

for _ in range(n - 1):
    u, v = map(int, sys.stdin.readline().split())
    u -= 1
    v -= 1
    edges.append((u, v))
    adj_list[u].append(v)
    adj_list[v].append(u)


# one cannot assume the root, so let's find the root
parent = [-1]*n 
parent[0] = 0 # root is its own parent

# use bfs to assign correct paths
queue = deque([0])
while queue:
    node = queue.popleft()
    for neighbor in adj_list[node]:
        if parent[neighbor] == -1:
            parent[neighbor] = node
            queue.append(neighbor)

tree = RootedTree(parent, 0)

k = int(sys.stdin.readline().strip())
path_count = [0]*n

for _ in range(k):
    a, b = map(int, sys.stdin.readline().split())
    a -= 1
    b -= 1
    path_count[a] += 1
    path_count[b] += 1
    l = tree.lca(a, b)
    if l:
        path_count[l] -= 2

edge_count: dict[tuple[int, int], int] = {}

def dfs(node: int, parent: int):
    for neighbor in adj_list[node]:
        if neighbor == parent:
            continue

        dfs(neighbor, node)
        path_count[node] += path_count[neighbor]
        edge_count[(min(node, neighbor), max(node, neighbor))] = path_count[neighbor]

dfs(0, -1)

result: list[str] = [str(edge_count[(min(u, v), max(u, v))]) for u, v in edges]

print(" ".join(result))