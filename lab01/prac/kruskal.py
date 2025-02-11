from dataclasses import dataclass
from typing import TypeVar, Generic
T = TypeVar("T")

@dataclass
class Edge(Generic[T]):
    x: T
    y: T
    weight: int

# implement unionfind
class UnionFind(Generic[T]):
    def __init__(self, nodes: list[T]):
        self.parent = {node: node for node in nodes}
        self.weight = {node: 1 for node in nodes}

    def find(self, i: T) -> T:
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])
            return self.parent[i]
        
    def union(self, i: T, j: T) -> bool:
        i_parent = self.find(i)
        j_parent = self.find(j)

        if i_parent == j_parent:
            return False
        
        # make i_parent weight always <= j_parent weight
        if self.weight[i_parent] > self.weight[j_parent]:
            i_parent, j_parent = j_parent, i_parent

        assert self.weight[i_parent] <= self.weight[j_parent]

        self.parent[i_parent] = j_parent # make j the new parent of i
        self.weight[j_parent] += self.weight[i_parent]

        return True

def kruskal(nodes: list[T], edges: list[Edge[T]]) -> list[Edge[T]]:
    sorted_edges = sorted(edges, key=lambda edge: edge.weight)

    uf = UnionFind(nodes)

    mst: list[Edge[T]] = []

    for edge in sorted_edges:
        if uf.union(edge.x, edge.y):
            mst.append(edge)

    return mst

print(kruskal([0, 1, 2, 3, 4], [
            Edge(0, 1, 4),
            Edge(1, 2, 2),
            Edge(0, 2, 4),
            Edge(0, 3, 6),
            Edge(2 ,3, 8),
            Edge(0, 4, 6),
            Edge(3, 4, 9),
        ]))

print(kruskal([0, 1, 2], [
            Edge(0, 1, -1),
            Edge(1, 2, 3),
            Edge(2, 0, -2)
        ]))




