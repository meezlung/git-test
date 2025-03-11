# type: ignore

from sample_graphs import T_ud_edgelist as T_el
from segtree import RangeSums


class TreeNode:
    def __init__(self, label):
        self.label: int = label
        self.children: list["TreeNode"] = []
        self.depth: int = 1
        self.w: int = 1
        self.parent: "TreeNode | None" = None
        self.top: "TreeNode | None" = None
        super().__init__()


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
    root = TreeNode(i)

    nodes = {}

    def _dfs(i, parent):
        vis[i] = True
        nodes[i] = parent
        heavy, heavy_i = -1, 0
        for j in adj[i]:
            if not vis[j]:
                child = TreeNode(j)
                child.parent = parent
                child.depth = parent.depth + 1
                parent.children.append(child)
                _dfs(j, child)
                parent.w += child.w
                if child.w > heavy:
                    heavy = child.w
                    heavy_i = len(parent.children) - 1
        if len(parent.children) > 1:
            parent.children[0], parent.children[heavy_i] = parent.children[heavy_i], parent.children[0]
            assert parent.children[0].w == max(n.w for n in parent.children)

    _dfs(i, root)
    root.parent = root
    return root, nodes


def compute_heavy_top(root, nodes):
    def _dfs(node):
        if node.parent is node:
            node.top = node
            return node.top
        elif node.parent.children[0] is not node:
            node.top = node
            return node.top
        elif node.top:
            return node.top
        else:
            node.top = _dfs(node.parent)
            return node.top
    for node in nodes.values():
        _dfs(node)


def flatten_heavy(root, nodes):
    lines = []
    index = 0
    idxs = {}
    def _dfs(node):
        nonlocal index
        idxs[node.label] = index
        lines.append(node.label)  # node.value
        index += 1
        for child in node.children:
            _dfs(child)
    _dfs(root)
    return lines, idxs


def compute_path_sum(u, v, nodes, idxs, rs):
    sm = 0
    u_n = nodes[u]
    v_n = nodes[v]
    while True:
        if u_n.top == v_n.top:
            i, j = idxs[u_n.label], idxs[v_n.label]
            sm += rs.sum(min(i, j), max(i, j) + 1)  # [i, j)
            break
        elif u_n.top.depth > v_n.top.depth:
            i, j = idxs[u_n.label], idxs[u_n.top.label]
            sm += rs.sum(min(i, j), max(i, j) + 1)
            u_n = u_n.top.parent
        else:
            i, j = idxs[v_n.label], idxs[v_n.top.label]
            sm += rs.sum(min(i, j), max(i, j) + 1)
            v_n = v_n.top.parent
    return sm


if __name__ == '__main__':
    adj = edgelist_to_adj(T_el)
    root, nodes = get_rooted_tree(adj, 0)
    compute_heavy_top(root, nodes)
    seq, indices = flatten_heavy(root, nodes)
    rs = RangeSums(seq)
    print(compute_path_sum(0, 11, nodes, indices, rs))