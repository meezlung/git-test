# type: ignore

from collections.abc import Sequence
from heapq import heappop, heappush
from math import inf

Corridor = tuple[tuple[int, int], int]

def make_adj_list(n: int, edges: Sequence[Corridor]):
    adj_list: dict[int, list[tuple[int, int]]] = {i: [] for i in range(1, n + 1)}

    for (i, j), weight in edges:
        adj_list[i].append((j, weight))
        adj_list[j].append((i, weight))

    return adj_list

def infiltrate(
        n: int,
        corridors: Sequence[Corridor],
        r: Sequence[int],
        s: int,
        e: int,
    ) -> int | None:

    adj_list = make_adj_list(n, corridors)
    teleporters = set(r)

    d: dict[int, float] = {i: inf for i in range(1, n + 1)}
    pq: list[tuple[int, int]] = [] # cost, i, j

    heappush(pq, (0, s))
    d[s] = 0

    visited_teleporters = False # to process teleporters once

    while pq:
        cost, i = heappop(pq)

        # if we've already considered a better way, ignore the current node
        if cost > d[i]:
            continue

        if i in teleporters and not visited_teleporters:
            for teleport in teleporters:
                if d[teleport] > cost:
                    d[teleport] = cost
                    heappush(pq, (cost, teleport))
            visited_teleporters = True # process teleporters once only

        for j, c in adj_list[i]:
            new_cost = cost + c
            if d[j] > new_cost:
                d[j] = new_cost
                heappush(pq, (new_cost, j))

    return d[e] if d[e] != inf else None