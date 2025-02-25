from collections import defaultdict
from collections.abc import Sequence

Teleporter = tuple[int, int]  # start, end


def max_grunts(g: Sequence[int], teleporters: Sequence[Teleporter]) -> int:
    n = len(g)

    adj: defaultdict[int, list[int]] = defaultdict(list)
    jda: defaultdict[int, list[int]] = defaultdict(list)

    for i, j in teleporters:
        adj[i].append(j)
        jda[j].append(i)

    def dfs(i: int, adj: defaultdict[int, list[int]], stack: list[int]):
        vis.add(i)
        for j in adj[i]:
            if j not in vis:
                dfs(j, adj, stack)

        stack.append(i)

    vis: set[int] = set()
    stack: list[int] = []

    for node in range(1, n + 1):
        if node not in vis:
            dfs(node, adj, stack)

    vis.clear()
    scc_tracker = [-1]*(n + 1)
    sccs: list[list[int]] = []
    scc_grunt_count: list[int] = []
    scc_count = 0

    while stack:
        node = stack.pop()
        if node not in vis:
            scc: list[int] = []
            dfs(node, jda, scc)
            sccs.append(scc)

            scc_grunt_sum = 0

            for n in scc:
                scc_tracker[n] = scc_count
                scc_grunt_sum += g[n - 1]

            scc_grunt_count.append(scc_grunt_sum)

            scc_count += 1

    # build scc-dag
    scc_graph: defaultdict[int, list[int]] = defaultdict(list)
    in_deg = [0] * scc_count

    for i, j in teleporters:
        if scc_tracker[i] != scc_tracker[j]: # edges between supernodes
            scc_graph[scc_tracker[i]].append(scc_tracker[j])
            in_deg[scc_tracker[j]] += 1

    # find longest path
    topo_order: list[int] = []
    zero_in_deg: list[int] = [i for i in range(scc_count) if in_deg[i] == 0]

    while zero_in_deg:
        i = zero_in_deg.pop()
        
        # visit
        topo_order.append(i)
        
        for j in scc_graph[i]:
            in_deg[j] -= 1
            if in_deg[j] == 0:
                zero_in_deg.append(j)

    dp = scc_grunt_count[:]
    print(dp)
    print(scc_graph)

    for node in topo_order:
        for neighbor in scc_graph[node]:
            dp[neighbor] = max(dp[neighbor], dp[node] + scc_grunt_count[neighbor])

    return max(dp)

print(max_grunts([0, 2, 3, 0], [
        (1, 2),
        (1, 3),
        (2, 4),
        (3, 4),
    ])
)

print(max_grunts([0, 2, 3, 0], [
        (1, 2),
        (2, 3),
        (3, 1),
        (2, 4),
        (3, 4),
    ])
)