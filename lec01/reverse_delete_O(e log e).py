from utils import Edge
from typing import Sequence, TypeVar, Generic

T = TypeVar("T")

class RollBackUnionFind(Generic[T]):
    def __init__(self, nodes: Sequence[T]):
        """ Initialize with each node separated and each weight """
        self.parent = {node: node for node in nodes}
        self.weight = {node: 1 for node in nodes}
        self.history: list[tuple[T, T, int, int]] = []
        self.component_count = len(nodes)

    def find(self, i: T) -> T:
        """ Return the parent of i """
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])
            return self.parent[i]
        
    def union(self, i: T, j: T) -> bool: 
        """ Returns true if union is successful. Otherwise, false. """
        i_parent = self.find(i)
        j_parent = self.find(j)

        if i_parent == j_parent:
            return False
        
        # Store prev weight of j before appending
        self.history.append((i_parent, j_parent, self.weight[j_parent], self.component_count))

        # Union by weight
        # Make one size the larger tree always
        if self.weight[i_parent] > self.weight[j_parent]:
            i_parent, j_parent = j_parent, i_parent

        assert self.weight[i_parent] <= self.weight[j_parent]

        self.parent[i_parent] = j_parent
        self.weight[j_parent] += self.weight[i_parent]

        self.component_count -= 1 # Merging reduces component count

        return True

    def rollback(self) -> bool:
        if not self.history:
            return False
        
        i_parent, j_parent, prev_weight_j, prev_component_count = self.history.pop()
        
        self.parent[i_parent] = i_parent 
        self.weight[j_parent] = prev_weight_j
        self.component_count = prev_component_count

        return True

def make_adj_list(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> dict[T, list[T]]:
    adj_list: dict[T, list[T]] = {node: [] for node in nodes}

    for edge in edges:
        adj_list[edge.x].append(edge.y)
        adj_list[edge.y].append(edge.x)
    
    return adj_list

def rev_del_mst_cost(nodes: Sequence[T], edges: Sequence[Edge[T]]) -> int:
    sorted_edges = sorted(edges, key=lambda x: x.weight, reverse=True)
    ruf = RollBackUnionFind(nodes)

    mst_cost = sum(edge.weight for edge in edges)

    for edge in sorted_edges:
        prev_components = ruf.component_count # Track components before removal

        if ruf.union(edge.x, edge.y):
            if ruf.component_count == prev_components: # If merging the two doesn't increase components
                ruf.rollback()
            else:
                mst_cost -= edge.weight

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