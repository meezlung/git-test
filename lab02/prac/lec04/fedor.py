
# type: ignore
from dataclasses import dataclass
import sys

@dataclass
class Edge:
    i: str
    j: str


def make_adj_list(nodes: list[str], edges: list[Edge]):
    adj_list: dict[str, list[tuple[str, Edge]]] = {node: [] for node in nodes}

    for edge in edges:
        adj_list[edge.i].append((edge.j, edge))
        # adj_list[edge.j].append((edge.i, edge))

    return adj_list


def sccs(nodes: list[str], edges: list[Edge]):

    n = len(nodes)
    adj = make_adj_list(nodes, edges)

    vis: list[bool] = [False] * n

    node_idx = {nodes[i]: i for i in range(n)}

    def dfs(i: str, adj: dict[str, list[tuple[str, Edge]]], stack: list[str]):
        assert not vis[node_idx[i]] 
        vis[node_idx[i]] = True

        for j, _ in adj[i]:
            if not vis[node_idx[j]]:
                dfs(j, adj, stack)

        stack.append(i)

    stack: list[str] = []

    for node in nodes:
        if not vis[node_idx[node]]:
            dfs(node, adj, stack)

    jda = make_adj_list(nodes, [
        Edge(edge.j, edge.i) for edge in edges
    ])
    
    vis: list[bool] = [False] * n

    while stack:
        i = stack.pop()
        if not vis[node_idx[i]]:
            scc: list[str] = []
            dfs(i, jda, scc)
            yield scc



m = int(sys.stdin.readline())
essay = sys.stdin.readline().split()

n = int(sys.stdin.readline())

_nodes: list[str] = []
_edges: list[Edge] = []

def choose_best_word(scc_groups):
    scc_map = {}
    for scc in scc_groups:
        # Select the best word: prioritize fewer 'r's, then shorter length
        best_word = min(scc, key=lambda word: (word.lower().count('r'), len(word)))
        for word in scc:
            scc_map[word] = best_word
    return scc_map

def transform_essay(essay, scc_map):
    transformed_essay = [scc_map.get(word, word) for word in essay]
    r_count = sum(word.lower().count('r') for word in transformed_essay)
    total_length = sum(len(word) for word in transformed_essay)
    return r_count, total_length

for _ in range(n):
    i,j = sys.stdin.readline().split()

    if i not in _nodes:
        _nodes.append(i)
    if j not in _nodes:
        _nodes.append(j)

    _edges.append(Edge(i, j))

print(_nodes)
print(_edges)

print(*sccs(_nodes, _edges))

sccs_grp = sccs(_nodes, _edges)
scc_map = choose_best_word(sccs_grp)
print(scc_map)

r_count, total_length = transform_essay(essay, scc_map)

print(r_count, total_length)