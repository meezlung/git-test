# type: ignore

import random

from sample_graphs import T_ud_centroid_el as T_el


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


def dfs_size(adj, i, p):
    sz = 1
    for j in adj[i]:
        if j != p and j not in banned:
            sz += dfs_size(adj, j, i)
    return sz


def dfs_centroid(adj, i):
    n = dfs_size(adj, i, None)
    centroid = None

    def _dfs(i, p):
        nonlocal centroid
        wi = 1
        ok_centroid = True

        for j in adj[i]:
            if j != p and j not in banned:
                wj = _dfs(j, i)
                wi += wj
                if wj * 2 > n:
                    ok_centroid = False
        if wi * 2 < n:
            ok_centroid = False
        if ok_centroid:
            centroid = i
        return wi

    _dfs(i, None)
    return centroid


def centroid_recurse(adj, i):
    centroid = dfs_centroid(adj, i)
    # for calculations that require the centroid, do it here
    banned.add(centroid)
    print(centroid, end=' ')
    for j in adj[centroid]:
        if j not in banned:
            centroid_recurse(adj, j)


adj = edgelist_to_adj(T_el)
banned = set()
centroid_recurse(adj, random.randint(0, len(adj) - 1))