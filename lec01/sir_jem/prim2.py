# type: ignore

from collections.abc import Sequence, Iterable

from heapq import heappush, heappop

# def heappush(pq, v):
#     pq.append(v)
#     loc = len(pq) - 1
#     while loc > 0:
#         parent = (loc - 1) // 2
#         if pq[parent] > pq[loc]:
#             pq[parent], pq[loc] = pq[loc], pq[parent]
#             loc = parent
#         else:
#             break


# def heappop(pq):
#     pq[0], pq[-1] = pq[-1], pq[0]
#     res = pq.pop()

#     loc = 0
#     while (son := loc * 2 + 1) < len(pq):
#         if son + 1 < len(pq) and pq[son + 1] < pq[son]:
#             son += 1
#         if pq[loc] > pq[son]:
#             pq[son], pq[loc] = pq[loc], pq[son]
#             loc = son
#         else:
#             break

#     return res

from utils import Edge, make_adjacency_list

def mst_cost[T](nodes, edges):
    # prim, fast
    adj = make_adjacency_list(nodes, edges)

    x = nodes[0]

    visited = set()

    pq = []

    heappush(pq, (0, x))

    ans = 0
    while pq:
        (cost, i) = heappop(pq)

        if i in visited:
            continue

        visited.add(i)
        ans += cost

        for j, c in adj[i]:
            heappush(pq, (c, j))

    return ans


assert mst_cost(range(5), [
        Edge(0, 1, 4),
        Edge(1, 2, 2),
        Edge(0, 2, 4),
        Edge(0, 3, 6),
        Edge(2 ,3, 8),
        Edge(0, 4, 6),
        Edge(3, 4, 9),
    ]) == 18

# if __name__ == '__main__':
#     for edge in mst_edges(range(5), [
#             Edge(0, 1, 4),
#             Edge(1, 2, 2),
#             Edge(0, 2, 4),
#             Edge(0, 3, 6),
#             Edge(2 ,3, 8),
#             Edge(0, 4, 6),
#             Edge(3, 4, 9),
#         ]):
#         print(edge)
