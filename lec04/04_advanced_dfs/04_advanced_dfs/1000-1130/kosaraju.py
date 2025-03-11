# type: ignore
from sample_graphs import G2_d_edgelist


def edgelist_to_adj(el, undirected=True):
    adj = {}
    for (i, j) in el:
        if i not in adj:
            adj[i] = []
        if j not in adj:
            adj[j] = []
        adj[i].append(j)
        if undirected:
            adj[j].append(i)
    return adj


def get_graph_transpose(adj):
    jda = {k: [] for k in adj.keys()}
    for k in adj:
        for i in adj[k]:
            jda[i].append(k)
    return jda


def kosaraju(adj):
    sccs = []
    curr_scc = []

    nodes = [*adj.keys()]

    disc = {}
    fin = {}
    parent = {}
    order = []
    tym = 1

    def _dfs(adj, i, p, first_pass):
        # - disc[i] is discovery time of i
        parent[i] = p
        nonlocal tym

        disc[i] = tym
        tym += 1
        if not first_pass:
            curr_scc.append(i)

        for j in adj[i]:
            if disc[j] is None:
                # (i,j) is tree edge
                _dfs(adj, j, i, first_pass)
            elif j != p:
                # (i,j) is back edge
                pass

        fin[i] = tym
        if first_pass:
            order.append(i)
        tym += 1


    # first pass
    disc = {n: None for n in nodes}
    for node in nodes:
        if disc[node] is None:
            _dfs(adj, node, None, True)
    # arrange nodes in decreasing order of finishing time
    order.reverse()

    # second pass
    jda = get_graph_transpose(adj)
    disc, fin, parent = {n: None for n in nodes}, {}, {}
    for node in order:
        if disc[node] is None:
            _dfs(jda, node, None, False)
            sccs.append(tuple(curr_scc))
            curr_scc = []
    return sccs

res = kosaraju(edgelist_to_adj(G2_d_edgelist, undirected=False))
print(res)
