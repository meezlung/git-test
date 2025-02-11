# type: ignore

from collections import defaultdict
from collections.abc import Sequence
from oj import Route, Result
from heapq import heappush, heappop

def edge_to_adj(edge_list):
    adj = defaultdict(list)
    for i, j, k in edge_list:
        if i not in adj:
            adj[i] = []
        if j not in adj:
            adj[j] = []
        adj[i].append((j,k))
    return dict(adj)

def answers(x: str, y: str, routes: Sequence[Route]) -> Result | None:
    if x == y:
        return Result(0,1,0,0)
    
    edges = []
    for route in routes:
        r, w = route
        u, v = r
        edges.append((u, v, w))
    
    adj_list = edge_to_adj(edges)

    MOD = 1_000_000_000

    if x not in adj_list or y not in adj_list:
        return None
    
    pq = [(0, x)]
    dist = {x: 0}
    count = {x: 1}
    min_edges = {x: 0}
    max_edges = {x: 0}

    while pq:
        d, node = heappop(pq)
        if node == y:
            continue

        for neighbor, weight in adj_list[node]:
            new_dist = d + weight
            
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                count[neighbor] = count[node]
                min_edges[neighbor] = min_edges[node] + 1
                max_edges[neighbor] = max_edges[node] + 1
                heappush(pq, (new_dist, neighbor))
            
            elif new_dist == dist[neighbor]:
                count[neighbor] = (count[neighbor] + count[node]) % MOD
                min_edges[neighbor] = min(min_edges[neighbor], min_edges[node] + 1)
                max_edges[neighbor] = max(max_edges[neighbor], max_edges[node] + 1)

    return Result(dist[y], count[y], min_edges[y], max_edges[y]) if y in dist else None