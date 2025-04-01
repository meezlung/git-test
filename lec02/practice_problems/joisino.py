import sys
from math import inf
from itertools import permutations

N, M ,R = map(int, sys.stdin.readline().split())
r = list(map(int, sys.stdin.readline().split()))

nodes = [i for i in range(N)]
node = {nodes[i] + 1: i for i in range(N)}

# i, j, c
edges: list[tuple[int, int, int]] = []

for _ in range(M):
    i, j, c = map(int, sys.stdin.readline().split())
    edges.append((i, j, c))

# floyd_warshall implementation
# n x n matrix w/ infinite
d = [[inf]*N for _ in range(N)]

# diagonal
for i in range(N):
    d[i][i] = 0

# actual values from edges
for i, j, c in edges:
    d[node[i]][node[j]] = min(d[node[i]][node[j]], c)
    d[node[j]][node[i]] = min(d[node[j]][node[i]], c)

# the dp formula
for k in range(N):
    for i in range(N):
        for j in range(N):
            d[i][j] = min(d[i][j], d[i][k] + d[k][j])

# bruteforce all possible paths that has r
min_distance = inf
for perm in permutations(r):
    cur_distance = sum(d[node[perm[i]]][node[perm[i + 1]]] for i in range(R - 1))
    min_distance = min(min_distance, cur_distance)

print(min_distance)