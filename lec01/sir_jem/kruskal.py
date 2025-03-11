# type: ignore

from collections.abc import Sequence, Iterable

from utils import Edge

class ConnectedComponents[T]:
    def __init__(self, nodes: Sequence[T]):
        # self.comps: list[set[T]] = [{i} for i in nodes]
        self.parent = {node: node for node in nodes}
        self.weight = {node: 1 for node in nodes}
        # super().__init__()

    def find(self, i: T):
        # return next(idx for idx, comp in enumerate(self.comps) if i in comp)
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])
            return self.parent[i]

    def union(self, i, j):
        # returns True if union is successful, false otherwise
        i = self.find(i)
        j = self.find(j)
        if i == j:
            return False

        # union by weight

        # make j the larger tree
        if self.weight[i] > self.weight[j]:
            i, j = j, i

        # j is now the larger tree (or equal)
        assert self.weight[i] <= self.weight[j]

        self.parent[i] = j
        self.weight[j] += self.weight[i]

        return True


def mst_edges[T](nodes: Sequence[T], edges: Sequence[Edge]) -> Iterable[Edge]:
    # sort the edges in increasing order of weight. (break ties arbitrarily)

    comps = ConnectedComponents(nodes)

    edges_chosen = []
    for edge in sorted(edges, key=lambda edge: edge.cost):
        if comps.union(edge.i, edge.j):
            edges_chosen.append(edge)
            yield edge

        # # verify if you want
        # assert connected_components(nodes, edges) == connected_components(nodes, edges_chosen)



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
