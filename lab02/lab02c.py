
from collections.abc import Sequence
from collections import defaultdict

Pair = tuple[str, str]

def best_types(info: Sequence[Pair]) -> set[str]:
    adj: defaultdict[str, list[str]] = defaultdict(list)
    jda: defaultdict[str, list[str]] = defaultdict(list)
    types: set[str] = set()

    for i, j in info:
        adj[i].append(j)
        jda[j].append(i)
        types.add(i)
        types.add(j)

    def dfs(i: str, adj: defaultdict[str, list[str]], stack: list[str]):
        vis.add(i)
        for j in adj[i]:
            if j not in vis:
                dfs(j, adj, stack)

        stack.append(i)

    vis: set[str] = set()
    stack: list[str] = []

    for node in types:
        if node not in vis:
            dfs(node, adj, stack)

    vis.clear()
    sccs: list[list[str]] = []
    node_to_scc: dict[str, int] = {}

    while stack:
        node = stack.pop()
        if node not in vis:
            scc: list[str] = []
            dfs(node, jda, scc)
            sccs.append(scc)

            # labelling for scc grps later
            scc_index = len(sccs) - 1
            for n in scc:
                node_to_scc[n] = scc_index

    scc_graph: defaultdict[int, set[int]] = defaultdict(set)
    in_deg = [0] * len(sccs)

    for i, j in info:
        scc_i, scc_j = node_to_scc[i], node_to_scc[j]
        if scc_i != scc_j:
            if scc_j not in scc_graph[scc_i]:  #that means may indeg sya
                scc_graph[scc_i].add(scc_j)
                in_deg[scc_j] += 1

    print(scc_graph)

    best_sccs = [i for i, deg in enumerate(in_deg) if deg == 0] # filter lahat ng walang may indeg(that means walang makakatalo sa kanya)

    print(best_sccs)

    if len(best_sccs) == 1: #there can only be one best
        return set(sccs[best_sccs[0]])
    
    return set() # if may multiple na best, wala 


best_types([("Fire", "Grass"), ("Grass", "Water"), ("H", "J")])
