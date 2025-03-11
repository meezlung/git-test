# type: ignore
from sample_graphs import G1_ud_edgelist


G_el = [
    (1, 2),
    (1, 3),
    (2, 5),
    (3, 4),
    (1, 4)
]


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


def bridges_and_articulation_points(adj):
    disc = {}
    fin = {}
    low = {}
    parent = {}
    tym = 1

    bridges = []
    articulation_points = []

    def _dfs(adj, i, p):
        # - disc[i] is discovery time of i
        # - low[i] is
        #   - lowest discovery time of any ancestor of i
        #   - reachable using a single back edge
        #   - from a descendant of i
        children = 0
        has_low_child = False
        parent[i] = p
        nonlocal tym
        disc[i] = low[i] = tym
        tym += 1

        for j in adj[i]:
            if disc[j] is None:
                # (i,j) is tree edge
                _dfs(adj, j, i)

                low[i] = min(low[i], low[j])
                children += 1

                if low[j] > disc[i]:
                    bridges.append((i, j))  # (i,j) is a bridge

                if low[j] >= disc[i]:
                    has_low_child = True

            elif j != p:
                # (i,j) is back edge
                low[i] = min(low[i], disc[j])

        if (p is None and children >= 2) or (p is not None and has_low_child):
            articulation_points.append(i)

        fin[i] = tym
        tym += 1

    nodes = [k for k in adj.keys()]
    for n in nodes:
        disc[n] = None

    for n in nodes:
        if disc[n] is None:
            _dfs(adj, n, None)

    return bridges, articulation_points


b, ap = bridges_and_articulation_points(edgelist_to_adj(G1_ud_edgelist))
print(b)
print(ap)
