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

def sssp_dijkstra(nodes: list[T], edges: list[Edge[T]], source: T) -> dict[T, float]:
    # make adj list
    adj: dict[T, list[tuple[T, int]]] = make_adj_list(nodes, edges)

    # visited bool hashmap
    # visited: list[bool] = [False] * len(nodes) # if ints ung nodes
    # however if in general
    visited: set[T] = set()

    # set of distances
    d: dict[T, float] = {node: inf for node in nodes}

    # pq (list of tuples of i and cost)
    pq: list[tuple[T, T | None, int]] = [] 

    # push the starting source to pq
    heappush(pq, (source, None, 0)) # first node as 0

    # while pq
    # pop a node from pq
    # assess that node
    # assess each neighbor of that node
      # push each neighbors to pq

    while pq:
        (i, j, cost) = heappop(pq)
        
        if i in visited:
            continue

        visited.add(i)
        d[i] = cost

        for j, c in adj[i]:
            heappush(pq, (j, i, cost + c))

    return d

print(sssp_dijkstra([0, 1, 2, 3, 4], [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, -1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ], 0))
print()

print(sssp_dijkstra([0, 1, 2, 3, 4, 5, 6, 7], [
        Edge(0, 1, 2),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(4, 5, 1),
        Edge(5, 6, 1),
        Edge(0, 7, 1),
        Edge(7, 6, 7),
    ], 0))
print()





