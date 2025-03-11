# type: ignore

from dataclasses import dataclass, field

from sample_graphs import G3_ud_edgelist as G3_el


@dataclass
class TreeNode:
    name: int
    children: list["TreeNode"] = field(default_factory=list)
    jumps: list[int] = field(default_factory=list)
    depth: int = 1
    p: "TreeNode | None" = None


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
        for j in adj[i]:
            if not vis[j]:
                child = TreeNode(j)
                child.p = parent
                child.depth = parent.depth + 1
                parent.children.append(child)
                _dfs(j, child)
    _dfs(i, root)
    root.p = root
    return root, nodes


def make_jump_pointers(nodes):
    n = len(nodes)
    pow_two, k = 1, 0
    while pow_two <= n:
        for i in range(n):
            node = nodes[i]
            if k == 0:
                node.jumps.append(node.p.name)
            else:
                jump1 = node.jumps[k - 1]
                jump1_node = nodes[jump1]
                jump2 = jump1_node.jumps[k - 1]
                node.jumps.append(jump2)
        pow_two *= 2
        k += 1


def lca(u, v, nodes):
    # Set v to be the "deeper" node
    u_node, v_node = nodes[u], nodes[v]
    if u_node.depth > v_node.depth:
        u, v = v, u
        u_node, v_node = v_node, u_node

    lgn = len(v_node.jumps)

    # Match v depth with u depth
    for k in reversed(range(lgn)):
        jump_k = v_node.jumps[k]
        node = nodes[jump_k]
        if node.depth >= u_node.depth:
            v = jump_k

    # u is an ancestor of v or vice versa
    if u == v:
        return u

    # Jump using the highest 2^k jumps possible without
    # overshooting past the LCA
    for k in reversed(range(lgn)):
        u_prime, v_prime = u_node.jumps[k], v_node.jumps[k]
        if u_prime != v_prime:
            u, v = u_prime, v_prime

    return nodes[u].p


def dist_on_tree(u, v, nodes):
    u_node, v_node = nodes[u], nodes[v]
    anc = lca(u, v, nodes)
    anc_node = nodes[anc]
    return u_node.depth + v_node.depth - (2 * anc_node.depth)


def euler_tour(root):
    tour = []
    def _euler_tour(root):
        tour.append(root.name)
        for node in root.children:
            _euler_tour(node)
            tour.append(root.name)
    _euler_tour(root)
    return tour


adj = edgelist_to_adj(G3_el)
root, nodes = get_rooted_tree(adj, 6)
make_jump_pointers(nodes)
for i in range(len(adj)):
    node = nodes[i]
    print(i, ':', node.jumps)


# U, V = 9, 10
for U in range(len(adj)):
    for V in range(U + 1, len(adj)):
        # print(U, V, dist_on_tree(U, V, nodes))
        ans = lca(U, V, nodes)
        print(f'LCA of {U} and {V} is {ans}')

# print(euler_tour(root))

