from dataclasses import dataclass
from typing import TypeVar, Generic
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


def dijkstra(nodes: list[T], edges: list[Edge[T]], source: T) -> dict[T, float]:
    adj_list = make_adj_list(nodes, edges)
    visited: set[T] = set()
    d: dict[T, float] = {node: inf for node in nodes}

    pq: list[tuple[T, T | None, int]] = []
    heappush(pq, (source, None, 0))

    total_cost = 0
    while pq:
        i, j, cost = heappop(pq)

        if i in visited:
            continue

        visited.add(i)
        d[i] = cost

        total_cost += cost

        for j, c in adj_list[i]:
            heappush(pq, (j, i, cost + c))

    return d

print(dijkstra([0, 1, 2, 3, 4], [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ], 0))
print()

