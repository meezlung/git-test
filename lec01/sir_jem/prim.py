# type: ignore

from collections.abc import Sequence, Iterable

from utils import Edge

def mst_edges[T](nodes: Sequence[T], edges: Sequence[Edge]) -> Iterable[Edge]:
    # prim
    # let x be an arbitrary node

    x = nodes[0]

    visited = {x}

    def good(edge):
        return edge.i in visited and edge.j not in visited or edge.i not in visited and edge.j in visited

    while len(visited) < len(nodes):
        edge = min((edge for edge in edges if good(edge)), key=lambda edge: edge.cost)

        visited.add(edge.i)
        visited.add(edge.j)

        yield edge


    # while not all nodes have been visited:
    #     let (i, j, c) be the cheapest edge where i has been visited and j has not been visited
    #     add that edge



def mst_cost[T](nodes, edges):
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
