import sys
from math import inf

N, M, L = map(int, sys.stdin.readline().split())

nodes = [i for i in range(N)]
node = {nodes[i] + 1: i for i in range(N)}

edges: list[tuple[int, int, int]] = []

for _ in range(M):
    i, j, c = map(int, sys.stdin.readline().split())
    edges.append((i, j, c))

d = [[inf]*N for _ in range(N)]

for i in range(N):
    d[i][i] = 0

for edge in edges:
    i, j, c = edge
    d[node[i]][node[j]] = min(d[node[i]][node[j]], c)
    d[node[j]][node[i]] = min(d[node[j]][node[i]], c)

for k in range(N):
    for i in range(N):
        for j in range(N):
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])

refuel_d = [[inf]*N for _ in range(N)]

for i in range(N):
    for j in range(N):
        if d[i][j] <= L:
            refuel_d[i][j] = 1 # only need 1 refuel if reachable within L

for k in range(N):
    for i in range(N):
        for j in range(N):
            refuel_d[i][j] = min(refuel_d[i][j], refuel_d[i][k] + refuel_d[k][j])

Q = int(sys.stdin.readline())

results: list[str] = []
for _ in range(Q):
    s, t = map(int, sys.stdin.readline(). split())

    if refuel_d[node[s]][node[t]] == inf:
        results.append("-1")
    else:
        results.append(str(refuel_d[node[s]][node[t]] - 1))

for r in results:
    print(r)