from utils import Edge
from typing import Sequence, TypeVar

T = TypeVar("T")

def make_adj_list(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> dict[T, list[T]]:
    adj_list: dict[T, list[T]] = {node: [] for node in nodes}

    for edge in edges:
        adj_list[edge.x].append(edge.y)
        adj_list[edge.y].append(edge.x)

    return adj_list

def dfs(adj_list: dict[T, list[T]], visited: set[T], start_node: T):
    visited.add(start_node)

    for neighbor in adj_list[start_node]:
        if neighbor not in visited:
            dfs(adj_list, visited, neighbor)

def is_connected(adj_list: dict[T, list[T]], nodes: Sequence[T]) -> bool:
    visited: set[T] = set()
    start_node = next(iter(nodes))
    dfs(adj_list, visited, start_node)
    return len(visited) == len(nodes)

def rev_del_mst_cost(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> int:
    sorted_edges = sorted(edges, key=lambda x: x.weight, reverse=True)
    adj_list = make_adj_list(nodes, edges)

    # Start with full MST of sorted edges
    mst_cost = 0
    mst: list[Edge[T]] = []
    for edge in sorted_edges:
        mst.append(edge)
        mst_cost += edge.weight

    # Keep removing edges depending if it makes it disconnected or not
    for edge in sorted_edges:
        e = edge
        mst.remove(edge)
        adj_list[edge.x].remove(edge.y)
        adj_list[edge.y].remove(edge.x)

        if not is_connected(adj_list, nodes):
            mst.append(e)
            adj_list[edge.x].append(edge.y)
            adj_list[edge.y].append(edge.x)
        else:
            mst_cost -= edge.weight

    for p in mst:
        print(p)

    return mst_cost

print(rev_del_mst_cost([0, 1, 2, 3, 4], [
            Edge(0, 1, 4),
            Edge(1, 2, 2),
            Edge(0, 2, 4),
            Edge(0, 3, 6),
            Edge(2 ,3, 8),
            Edge(0, 4, 6),
            Edge(3, 4, 9),
        ]))