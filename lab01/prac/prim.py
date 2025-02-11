from dataclasses import dataclass
from typing import TypeVar, Generic
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

def prim(nodes: list[T], edges: list[Edge[T]]) -> list[Edge[T]]:
    adj_list = make_adj_list(nodes, edges)
    visited: set[T] = set()
    path: list[Edge[T]] = []

    # heap
    pq: list[tuple[T, T | None, int]] = [] # (i, j, cost)
    heappush(pq, (nodes[0], None, 0))

    total_cost = 0
    while pq:
        (i, j, cost) = heappop(pq)

        if i in visited: # don't revisit nodes
            continue

        visited.add(i)

        if j is not None:
            path.append(Edge(j, i, cost))

        total_cost += cost

        for j, c in adj_list[i]:
            heappush(pq, (j, i, c))

    return path

print(prim([0, 1, 2, 3, 4], [
            Edge(0, 1, 4),
            Edge(1, 2, 2),
            Edge(0, 2, 4),
            Edge(0, 3, 6),
            Edge(2 ,3, 8),
            Edge(0, 4, 6),
            Edge(3, 4, 9),
        ]))

print(prim([0, 1, 2], [
            Edge(0, 1, -1),
            Edge(1, 2, 3),
            Edge(2, 0, -2)
        ]))

    
