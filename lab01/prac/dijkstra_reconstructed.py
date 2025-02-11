from dataclasses import dataclass
from typing import Generic, TypeVar
from math import inf
from heapq import heappush, heappop
T = TypeVar("T")

@dataclass
class Edge(Generic[T]):
    x: T
    y: T
    weight: int

def make_adj_list(nodes: list[T], edges: list[Edge[T]], directed: bool = False) -> dict[T, list[tuple[T, int]]]:
    adj_list: dict[T, list[tuple[T, int]]] = {node: [] for node in nodes}

    for edge in edges:
        adj_list[edge.x].append((edge.y, edge.weight))
        if not directed:
            adj_list[edge.y].append((edge.x, edge.weight))

    return adj_list

def dijkstra(nodes: list[T], edges: list[Edge[T]], source: T) -> tuple[dict[T, float], dict[T, T | None]]:
    adj_list = make_adj_list(nodes, edges)
    d: dict[T, float] = {node: inf for node in nodes}
    d[source] = 0
    parent: dict[T, T | None] = {node: None for node in nodes}

    pq: list[tuple[T, float]] = []
    heappush(pq, (source, 0)) # i, cost

    while pq:
        i, cost = heappop(pq)

        # try to uncomment this
        if cost > d[i]:
            continue

        for j, c in adj_list[i]:
            if d[i] + c < d[j]:
                d[j] = d[i] + c
                parent[j] = i
                heappush(pq, (j, d[j]))

    return d, parent

def reconstruct_path(parent: dict[T, T | None], target: T | None) -> list[T]:
    path: list[T] = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]

def dijkstra_rec(nodes: list[T], edges: list[Edge[T]], source: T) -> None:
    d, parent = dijkstra(nodes, edges, source)

    print("Path for each shortest distance from source")

    for node in nodes:
        path = reconstruct_path(parent, node)

        if d[node] != inf:
            print(f"Path to {node}:", path)
        else:
            print("Unreachable!")

print(dijkstra_rec([0, 1, 2, 3, 4], [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ], 0))
print()




