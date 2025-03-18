# type: ignore

from collections import deque
from dataclasses import dataclass

from sample_graphs import G_ud_matching as G_m
from sample_graphs import G_ud_matching_2 as G_m2
from sample_graphs import G_ud_matching_3of4 as G_m3


@dataclass
class Edge:
    i: int
    j: int
    cap: int
    back: "Edge | None" = None
    flow: int = 0

    @property
    def residual(self):
        return self.cap - self.flow

    def push_flow(self, f):
        self.flow += f
        if self.back:
            self.back.flow -= f
    


def edgelist_to_adj(n, el):
    adj = {i: [] for i in range(n)}
    for i, j in el:
        adj[i].append(j)
        adj[j].append(i)
    return adj


def get_bipartite(n, adj):
    lr = ([], [])
    vis = [-1] * n
    color = 0

    def _dfs(i, p, color):
        # 2-coloring to check bipartiteness
        vis[i] = color
        good = True

        for j in adj[i]:
            if j != p:
                if vis[j] == -1:
                    good = _dfs(j, i, (color + 1) % 2)
                elif vis[j] == vis[i]:
                    good = False
            if not good:
                break

        lr[vis[i]].append(i)
        return good

    for i in range(n):
        if vis[i] == -1:
            ok = _dfs(i, None, 0)
            if not ok:
                return False, ([], [])
    return True, lr


def kuhn_bipartite_matching(n, adj, L, R):
    mtch = [-1] * n

    def _find_aug_path(i):
        if not vis[i]:
            vis[i] = True
            for j in adj[i]:
                if mtch[j] == -1 or _find_aug_path(mtch[j]):
                    mtch[j] = i
                    return True
        return False

    ans = 0
    for i in L:
        vis = [False] * n
        if _find_aug_path(i):
            ans += 1
    return ans, tuple((r, mtch[r]) for r in R if mtch[r] != -1)


def flow_bipartite_matching(n, adj):
    # compute maximum matching using maxflow
    ok, (L, R) = get_bipartite(n, adj)
    if not ok:
        raise Exception('Graph is not bipartite.')

    def _make_flow_edges(i, j, c):
        edge = Edge(i, j, c)
        egde = Edge(j, i, 0)
        edge.back = egde
        egde.back = edge
        return (edge, egde)

    def _augment_path(i, min_cap):
        nonlocal found
        vis[i] = True

        if i == T:
            found = True
            return min_cap

        edges = (e for e in flow_adj[i] if e.j not in vis and e.residual > 0)
        for edge in edges:
            min_cap = _augment_path(edge.j, min(min_cap, edge.residual))
            if found:
                edge.push_flow(min_cap)
                return min_cap

        return min_cap
            

    S, T = -1, n
    flow_adj = {
        S: [], T:[],
        **{i: [] for i in range(n)}
    }
    for i in L:
        ij, ji = _make_flow_edges(S, i, 1)
        flow_adj[S].append(ij)
        flow_adj[i].append(ji)

        for j in adj[i]:
            ij, ji = _make_flow_edges(i, j, 1)
            flow_adj[i].append(ij)
            flow_adj[j].append(ji)
    for i in R:
        ij, ji = _make_flow_edges(i, T, 1)
        flow_adj[i].append(ij)
        flow_adj[T].append(ji)
    
    max_flow = 0
    while True:
        vis = {S: True}
        found = False
        flow = _augment_path(S, float('inf'))
        if not found:
            break
        max_flow += flow
    matching = []
    for l_node in L:
        for edge in flow_adj[l_node]:
            if edge.flow > 0 and edge.residual == 0:
                matching.append((edge.i, edge.j))
    return max_flow, matching


def stable_matching(doer_prefs, rcvr_prefs):
    # Gale-Shapely algorithm
    # The "doers" initiate requests
    # The "receivers" accept/reject requests
    # Please double check this implementation; may contain bugs
    n = len(doer_prefs)

    assert n == len(rcvr_prefs)
    for i in range(n):
        assert n == len(doer_prefs[i]) == len(rcvr_prefs[i])

    doer_mark = [False] * n
    rcvr_choice = [-1] * n

    ranks = [0] * n

    for rnd in range(n * n):
        rcvr_candidates = [[] for _ in range(n)]

        for doer in range(n):
            rank = ranks[doer]
            prefs = doer_prefs[doer]
            if not doer_mark[doer]:
                rcvr_candidates[prefs[rank]].append(doer)
                ranks[doer] += 1
        for rcvr in range(n):
            prefs = rcvr_prefs[rcvr]
            cands = [(i, prefs.index(i)) for i in rcvr_candidates[rcvr]]
            if cands:
                choice = min(cands, key=lambda t: t[1])[0]
                if rcvr_choice[rcvr] != -1:
                    prev_choice = rcvr_choice[rcvr]
                    doer_mark[prev_choice] = False
                rcvr_choice[rcvr] = choice
                doer_mark[choice] = True
    return [(rcvr_choice[i], i) for i in range(n)]


n, el = G_m2
adj = edgelist_to_adj(n, el)

max_matching, matching = flow_bipartite_matching(n, adj)
print('Max matching using flow')
print(max_matching, matching)


# If you don't have the two sets of the bipartite graph yet
print('Getting two sets of bipartite graph')
ok, (L, R) = get_bipartite(n, adj)
print(L)
print(R)
if ok:
    sz, matching = kuhn_bipartite_matching(n, adj, L, R)
    print(sz)
    print(matching)
else:
    raise Exception('The graph provided is not bipartite.')

student_prefs = [
    [1, 0, 2],
    [1, 2, 0],
    [2, 1, 0]
]
students = ['Adam', 'Bruno', 'Charlie']

lab_prefs = [
    [1, 2, 0],
    [2, 0, 1],
    [1, 2, 0]
]
labs = ['SCL', 'CVMIL', 'NDSL']

print('Stable Matching')
print('---')
print('Student prefs')
for i in range(3):
    print(students[i], ':', [labs[j] for j in student_prefs[i]])
print('Lab prefs')
for i in range(3):
    print(labs[i], ':', [students[j] for j in lab_prefs[i]])
result = stable_matching(student_prefs, lab_prefs)
print([(students[i], labs[j]) for i, j in result])
