# type: ignore

from collections.abc import Iterable, Sequence

from utils import Edge

def mst_edges[T](nodes: Sequence[T], edges: Sequence[Edge]) -> Iterable[Edge]:

    mst_cost = 0
    adj = {node: [] for node in nodes}

    def add_edge(edge):
        nonlocal mst_cost
        mst_cost += edge.cost
        adj[edge.i].append((edge.j, edge.cost))
        adj[edge.j].append((edge.i, edge.cost))

    def get_comps():
        comp = {}
        comp_ct = 0
        for s in nodes:
            if s not in comp:
                comp_ct += 1
                comp[s] = s
                stak = [s]
                while stak:
                    i = stak.pop()
                    assert comp[i] == s
                    for j, c in adj[i]:
                        if j not in comp:
                            comp[j] = s
                            stak.append(j)
                        assert comp[j] == s

        return comp, comp_ct

    inc = [False]*len(edges)
    while True:

        # get components
        comp, comp_ct = get_comps()

        if comp_ct <= 1:
            break

        # get minimum edge away from each component, tie-break by edge index
        min_edge = {node: (float('inf'), None) for node in nodes}

        for idx, edge in enumerate(edges):
            if comp[edge.i] != comp[edge.j]:
                min_edge[comp[edge.i]] = min(min_edge[comp[edge.i]], (edge.cost, idx))
                min_edge[comp[edge.j]] = min(min_edge[comp[edge.j]], (edge.cost, idx))

        for c, idx in min_edge.values():
            if idx is not None and not inc[idx]:
                inc[idx] = True
                add_edge(edges[idx])
                yield edges[idx]

    return mst_cost


def mst_cost[T](nodes: Sequence[T], edges: Sequence[Edge]) -> int:
    return sum(edge.cost for edge in mst_edges(nodes, edges))


assert mst_cost(range(5), [
        Edge(0, 1, 4),
        Edge(1, 2, 2),
        Edge(0, 2, 4),
        Edge(0, 3, 6),
        Edge(2 ,3, 8),
        Edge(0, 4, 6),
        Edge(3, 4, 9),
    ]) == 18

if __name__ == '__main__':
    for edge in mst_edges(range(5), [
            Edge(0, 1, 4),
            Edge(1, 2, 2),
            Edge(0, 2, 4),
            Edge(0, 3, 6),
            Edge(2 ,3, 8),
            Edge(0, 4, 6),
            Edge(3, 4, 9),
        ]):
        print(edge)
