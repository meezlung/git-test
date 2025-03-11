from utils import Edge
from typing import Sequence, TypeVar, Generic, Iterable

T = TypeVar("T")

class UnionFind(Generic[T]):
    def __init__(self, nodes: Sequence[T]):
        """ Initialize with each node separated and each weight """
        self.parent = {node: node for node in nodes}
        self.weight = {node: 1 for node in nodes}

    def find(self, i: T) -> T:
        """ Return the parent of i using path compression """
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])
            return self.parent[i]
        
    def union(self, i: T, j: T) -> bool: 
        """ Returns true if union is successful. Otherwise, false. """
        i_parent = self.find(i)
        j_parent = self.find(j)

        if i_parent == j_parent: # If the two edges are from the same group
            return False
        
        # Union by weight
        # Make one size the larger tree always
        if self.weight[i_parent] > self.weight[j_parent]:
            i_parent, j_parent = j_parent, i_parent

        assert self.weight[i_parent] <= self.weight[j_parent]

        self.parent[i_parent] = j_parent # Read it as put i_parent to j_parent, in a way we're putting the reference of i_parent to j_parent
        self.weight[j_parent] += self.weight[i_parent]

        # print(self.parent)
        # print(self.weight)

        return True

def kruskal_mst_edges(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> Iterable[Edge[T]]:
    # Sort by weight
    sorted_edges: Sequence[Edge[T]] = sorted(edges, key=lambda x: x.weight)

    components = UnionFind(nodes)

    for edge in sorted_edges:
        if components.union(edge.x, edge.y):
            yield edge

def kruskal_mst_cost(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> int:
    mst = kruskal_mst_edges(nodes, edges)
    total_cost = 0
    for edge in mst:
        print(edge)
        total_cost += edge.weight

    return total_cost

print(kruskal_mst_cost([0, 1, 2, 3, 4], [
            Edge(0, 1, 4),
            Edge(1, 2, 2),
            Edge(0, 2, 4),
            Edge(0, 3, 6),
            Edge(2 ,3, 8),
            Edge(0, 4, 6),
            Edge(3, 4, 9),
        ]))