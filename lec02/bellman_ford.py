from utils import Edge
from typing import TypeVar
from math import inf

T = TypeVar("T")

def sssp_bellman_ford(nodes: list[T], edges: list[Edge[T]], source: T) -> dict[T, float]:
    d: dict[T, float] = {edge.x: inf for edge in edges} # initializes for nodes only present in x nodes
    d.update({edge.y: inf for edge in edges}) # so we must also add those y nodes
    d[source] = 0

    print("bruh1", d)

    def augment():
        augmented = False
        for edge in edges:
            if d[edge.x] < inf and d[edge.y] > d[edge.x] + edge.weight:
                d[edge.y] = d[edge.x] + edge.weight
                augmented = True
        return augmented

    # relax all edges of n - 1 edges
    for _ in range(len(nodes) - 1):
        if not augment():
            print("Goods!")
            return d # Early termination if no augments occur
        
        
    print("There's a negative cycle.")
    return d

    ...

print(sssp_bellman_ford([0, 1, 2, 3, 4], [
        Edge(0, 1, 1),
        Edge(1, 2, 1),
        Edge(2, 3, -1),
        Edge(3, 4, 1),
        Edge(3, 1, 1),
    ], 0))

print(sssp_bellman_ford([0, 1, 2, 3, 4, 5, 6, 7], [
        Edge(0, 1, 2),
        Edge(1, 2, 1),
        Edge(2, 3, 1),
        Edge(3, 4, 1),
        Edge(4, 5, 1),
        Edge(5, 6, 1),
        Edge(0, 7, 1),
        Edge(7, 6, 7),
    ], 0))