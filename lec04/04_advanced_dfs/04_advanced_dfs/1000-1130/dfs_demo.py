# type: ignore
from sample_graphs import G1_ud_edgelist


def edgelist_to_adj(el, ignored_edges=[], ignored_nodes=[], undirected=True):
	adj = {}
	for i, j in el:
		if i not in adj:
			adj[i] = []
		if j not in adj:
			adj[j] = []
		if (i, j) not in ignored_edges and i not in ignored_nodes and j not in ignored_nodes:
			adj[i].append(j)
			if undirected and (j, i) not in ignored_edges:
				adj[j].append(i)
	return adj

vis = {}

bridges = []
articulation_points = []


def dfs(adj, i):
	vis[i] = True
	for j in adj[i]:
		if j not in vis:
			dfs(adj, j)

# brute force bridges
for ind in range(len(G1_ud_edgelist)):
	e = G1_ud_edgelist[ind]
	vis.clear()
	adj = edgelist_to_adj(G1_ud_edgelist, ignored_edges=[e])
	dfs(adj, 1)
	if len(vis) < len(adj):
		bridges.append(e)
print(bridges)


# brute force articulation points
full_adj = edgelist_to_adj(G1_ud_edgelist)
nodes = [*full_adj.keys()]
for node in nodes:
	vis.clear()
	adj = edgelist_to_adj(G1_ud_edgelist, ignored_nodes=[node])
	dfs(adj, (node % len(adj)) + 1)  # do not start DFS in excluded node
	if len(vis) < len(adj) - 1:
		articulation_points.append(node)
print(articulation_points)


# dfs(edgelist_to_adj(G1_ud_edgelist), 1)
# print(vis)
# print(all(vis.values()))