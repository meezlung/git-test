# type: ignore

from collections import deque
from dataclasses import dataclass

from sample_graphs import G_d_flow1_el as flow1_el
from sample_graphs import G_d_flow2_el as flow2_el
from sample_graphs import G_d_flow4_el as flow4_el


@dataclass
class Edge:
    fro: int
    to: int
    capacity: int
    flow: int = 0
    back: "Edge | None" = None

    @property
    def residual(self):
        return self.capacity - self.flow


def edgelist_to_adj(el):
    adj = {}
    for u, v, c in el:
        if u not in adj:
            adj[u] = []
        if v not in adj:
            adj[v] = []
        edge = Edge(u, v, c)
        egde = Edge(v, u, 0)
        edge.back = egde
        egde.back = edge
        adj[u].append(edge)
        adj[v].append(egde)
    return adj


def reset_flow(adj):
    for node in adj:
        for edge in adj[node]:
            edge.flow = 0


def greedy_augmenting_path(s, t, adj):
    # This augmentation method is incorrect
    found = False
    vis = set()

    def _dfs(i, min_cap):
        nonlocal found
        vis.add(i)
        if i == t:
            found = True
            return min_cap
        else:
            edges = (e for e in adj[i] if e.to not in vis and e.residual > 0)
            for edge in edges:
                min_cap = _dfs(edge.to, min(min_cap, edge.residual))
                if found:
                    edge.flow += min_cap
                    # edge.back.flow -= min_cap
                    return min_cap
        return min_cap

    result = _dfs(s, float('inf'))
    return found, result


def find_augmenting_path(s, t, adj):
    found = False
    vis = set()

    def _dfs(i, min_cap):
        nonlocal found
        vis.add(i)
        if i == t:
            found = True
            return min_cap
        else:
            edges = (e for e in adj[i] if e.to not in vis and e.residual > 0)
            for edge in edges:
                min_cap = _dfs(edge.to, min(min_cap, edge.residual))
                if found:
                    edge.flow += min_cap
                    edge.back.flow -= min_cap
                    return min_cap
        return min_cap

    result = _dfs(s, float('inf'))
    return found, result


def bfs_augmenting_path(s, t, adj):
    vis = set([s])
    kyu = deque([s])
    pred = {s: None}

    while kyu:
        u = kyu.popleft()
        edges = (e for e in adj[u] if e.to not in vis and e.residual > 0)
        for edge in edges:
            vis.add(edge.to)
            kyu.append(edge.to)
            pred[edge.to] = edge

    if t not in vis:
        return False, float('inf')
    min_cap = float('inf')
    v = t
    edges_to_update = []
    while v != s:
        e = pred[v]
        edges_to_update.append(e)
        min_cap = min(min_cap, e.residual)
        v = e.fro
    for edge in edges_to_update:
        edge.flow += min_cap
        edge.back.flow -= min_cap
    return True, min_cap


def greedy_maxflow(s ,t, adj):
    # WARNING! THIS ALGORITHM IS AN INCORRECT GREEDY SOLUTION
    max_flow = 0
    while True:
        success, flow = greedy_augmenting_path(s, t, adj)
        if not success:
            break
        max_flow += flow
    return max_flow


def ford_fulkerson(s, t, adj):
    max_flow = 0
    while True:
        success, flow = find_augmenting_path(s, t, adj)
        if not success:
            break
        max_flow += flow
    return max_flow


def edmonds_karp(s, t, adj):
    max_flow = 0
    while True:
        success, flow = bfs_augmenting_path(s, t, adj)
        if not success:
            break
        max_flow += flow
    return max_flow


adj = edgelist_to_adj(flow4_el)
print(greedy_maxflow(0, 3, adj))

reset_flow(adj)
print(ford_fulkerson(0, 3, adj))

reset_flow(adj)
print(edmonds_karp(0, 3, adj))

