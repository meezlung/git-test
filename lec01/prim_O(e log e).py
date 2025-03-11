from utils import Edge
from typing import Sequence, TypeVar
from heapq import heappush, heappop

T = TypeVar("T")

def make_adj_list(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> dict[T, list[tuple[T, int]]]:
    adj_list: dict[T, list[tuple[T, int]]] = {node: [] for node in nodes}

    for edge in edges:
        adj_list[edge.x].append((edge.y, edge.weight))
        adj_list[edge.y].append((edge.x, edge.weight))
    
    return adj_list

def prim_mst_cost(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> int:
    # Prim, Fast
    adj_list = make_adj_list(nodes, edges)
    visited: set[T] = set()
    path: list[Edge[T]] = []

    prim_heap: list[tuple[int, T, T | None]] = []
    heappush(prim_heap, (0, nodes[0], None)) # (cost, first node)

    total_cost = 0
    while prim_heap:
        (cost, i, j) = heappop(prim_heap)

        if i in visited:
            continue

        visited.add(i)

        if j is not None:
            path.append(Edge(j, i, cost))

        total_cost += cost

        for j, c in adj_list[i]:
            heappush(prim_heap, (c, j, i))

    for p in path:
        print(p)

    return total_cost

print(prim_mst_cost([0, 1, 2, 3, 4], [
            Edge(0, 1, 4),
            Edge(1, 2, 2),
            Edge(0, 2, 4),
            Edge(0, 3, 6),
            Edge(2 ,3, 8),
            Edge(0, 4, 6),
            Edge(3, 4, 9),
        ]))