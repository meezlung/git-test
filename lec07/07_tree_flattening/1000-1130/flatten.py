# type: ignore


import random

from dataclasses import dataclass, field

from sample_graphs import G3_ud_edgelist as T1_el
from sample_graphs import T_ud_edgelist as T2_el

from segtree import RangeSums as RS
from segtree_min import RangeMin as RM


@dataclass
class TreeNode:
    label: int
    v: int
    children: list["TreeNode"] = field(default_factory=list)
    depth: int = 1
    parent: "TreeNode | None" = None


def edgelist_to_adj(el):
    adj = {}
    for i, j in el:
        if i not in adj:
            adj[i] = []
        if j not in adj:
            adj[j] = []
        adj[i].append(j)
        adj[j].append(i)
    return adj


def get_rooted_tree(adj, i):
    n = len(adj)
    vis = [False] * n
    root = TreeNode(i, i)

    nodes = {}

    def _dfs(i, parent):
        vis[i] = True
        nodes[i] = parent
        for j in adj[i]:
            if not vis[j]:
                child = TreeNode(j, j)
                child.parent = parent
                child.depth = parent.depth + 1
                parent.children.append(child)
                _dfs(j, child)
    _dfs(i, root)
    root.parent = root
    return root, nodes


def preorder(root):
    flat = []
    def _preorder(root):
        root.lindex = len(flat)
        flat.append(root.v)
        for child in root.children:
            _preorder(child)
        root.rindex = len(flat)
    _preorder(root)
    return flat


root1, nodes1 = get_rooted_tree(edgelist_to_adj(T1_el), 6)
seq1 = preorder(root1)
print(seq1)
rs = RS(seq1)
rm = RM(seq1)

print('Perform subtree queries using range sum and range min')
for i in range(len(nodes1)):
    node = nodes1[i]
    print(f'Sum of subtree of node {i} = {rs.sum(node.lindex, node.rindex)}')
    print(f'Min of subtree of node {i} = {rm.range_min(node.lindex, node.rindex)}')

print('random updates')

for i in range(len(nodes1)):
    node = nodes1[i]
    node.v = random.randint(1, 50)
    print(f'New value of node {i} = {node.v}')
    rs.set(node.lindex, node.v)
    rm.set(node.lindex, node.v)

print('Subtree queries again...')
for i in range(len(nodes1)):
    node = nodes1[i]
    print(f'Sum of subtree of node {i} = {rs.sum(node.lindex, node.rindex)}')
    print(f'Min of subtree of node {i} = {rm.range_min(node.lindex, node.rindex)}')