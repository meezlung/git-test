from utils import Edge
from typing import TypeVar
from math import inf
from heapq import heappush, heappop

T = TypeVar("T")

def make_adj_list(nodes: list[T], edges: list[Edge[T]]) -> dict[T, list[tuple[T, int]]]:
    adj: dict[T, list[tuple[T, int]]] = {node: [] for node in nodes}

    for edge in edges:
        adj[edge.x].append((edge.y, edge.weight))
        adj[edge.y].append((edge.x, edge.weight))

    return adj

def sssp_dijkstra(nodes: list[T], edges: list[Edge[T]], source: T) -> tuple[dict[T, float], dict[T, T | None]]:
    # make adj list
    adj: dict[T, list[tuple[T, int]]] = make_adj_list(nodes, edges)

    # set of distances
    d: dict[T, float] = {node: inf for node in nodes}
    d[source] = 0

    # pq (list of tuples of i and cost)
    pq: list[tuple[float, T]] = [] 

    # NEW: add a parent to track path
    parent: dict[T, T | None] = {node: None for node in nodes}

    # push the starting source to pq
    heappush(pq, (0, source)) # first node as 0

    # while pq
    # pop a node from pq
    # assess that node
    # assess each neighbor of that node
      # push each neighbors to pq

    while pq:
        (cost, i) = heappop(pq)
        
        if cost > d[i]:
            continue

        for j, c in adj[i]:
            if d[i] + c < d[j]: # relaxation step
                d[j] = d[i] + c
                parent[j] = i # track the prev node
                heappush(pq, (d[j], j))

    return d, parent

def reconstruct_path(parent: dict[T, T | None], target: T | None) -> list[T]:
    path: list[T] = []
    while target is not None:
        path.append(target)
        target = parent[target]

    return path[::-1]  

def dijkstra_reconstructed(nodes: list[T], edges: list[Edge[T]], source: T) -> None:
    d, parent = sssp_dijkstra(nodes, edges, source)

    print("Shortest distances: ", d)

    for node in nodes:
        path = reconstruct_path(parent, node)
        print(f"Path to {node}:", path if d[node] != inf else "Unreachable")

    print()

print("SSSP")
dijkstra_reconstructed([0, 1, 2, 3, 4], [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ], 0)
print()

dijkstra_reconstructed([0, 1, 2, 3, 4, 5, 6, 7], [
        Edge(0, 1, 2),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(4, 5, 1),
        Edge(5, 6, 1),
        Edge(0, 7, 1),
        Edge(7, 6, 7),
    ], 0)
print()





