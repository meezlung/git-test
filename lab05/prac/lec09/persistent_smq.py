from math import inf
from collections.abc import Sequence
from dataclasses import dataclass, field

class RMQ:
    def __init__(self, i: int, j: int, min_value: int, l: "RMQ | None" = None, r: "RMQ | None" = None):
        self.i = i
        self.j = j
        self.min_value = min_value
        self.l = l
        self.r = r

    @staticmethod
    def build(seq: Sequence[int], i: int, j: int) -> "RMQ":
        if j - i == 1:
            return RMQ(i, j, seq[i])
        k = (i + j) // 2
        l = RMQ.build(seq, i, k)
        r = RMQ.build(seq, k, j)
        return RMQ(i, j, min(l.min_value, r.min_value), l, r)

    def get(self, i: int) -> int:
        if self.j - self.i == 1:
            return self.min_value
        else: 
            assert self.l is not None and self.r is not None
    
            if i < self.r.i:
                return self.l.get(i)
            else:
                return self.r.get(i)
        
    def set(self, i: int, v: int) -> "RMQ":
        if not (self.i <= i < self.j):
            return self
        if self.j - self.i == 1:
            # create a new leaf with the updated value
            return RMQ(self.i, self.j, v)
        
        assert self.l is not None and self.r is not None

        new_l = self.l.set(i, v) if i < self.r.i else self.l
        new_r = self.r.set(i, v) if i >= self.r.i else self.r
        return RMQ(self.i, self.j, min(new_l.min_value, new_r.min_value), new_l, new_r)

    def range_min(self, i: int, j: int) -> float:
        if i <= self.i and self.j <= j:
            return self.min_value
        elif j <= self.i or self.j <= i:
            return inf
        else:
            assert self.l is not None and self.r is not None

            lmin = self.l.range_min(i, j)
            rmin = self.r.range_min(i, j)
            return min(lmin, rmin)
        

class PersistentRMQ:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.root = RMQ.build(values, 0, self.n)

    def __len__(self):
        return self.n
    
    def range_min(self, i: int, j: int):
        assert 0 <= i <= j <= self.n
        return self.root.range_min(i, j)
    
    def update(self, i: int, v: int) -> "PersistentRMQ":
        assert 0 <= i < self.n
        new_rmq = PersistentRMQ.__new__(PersistentRMQ)
        new_rmq.n = self.n
        new_rmq.root = self.root.set(i, v)
        return new_rmq
    
    def __getitem__(self, i: int) -> int:
        assert 0 <= i < self.n
        return self.root.get(i)
    


@dataclass
class Node:
    label: int
    value: int
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)
    index: int = -1   # pre-order start index
    rindex: int = -1  # pre-order end index

    def preorder(self, pre: "list[Node]") -> None:
        self.index = len(pre)  # record left index in pre-order
        pre.append(self)
        for child in self.children:
            child.preorder(pre)
        self.rindex = len(pre)  # record right index in pre-order


class PersistentSMQ:
    def __init__(self, values: Sequence[int], root: int, parent: Sequence[int]):
        self.n = len(values)
        # Build nodes for each value
        self.nodes = [Node(label=i, value=values[i]) for i in range(self.n)]

        # Initialize root node
        self.root = self.nodes[root]

        # Set parent pointers for all nodes
        for i in range(self.n):
            self.nodes[i].parent = self.nodes[parent[i]]
        
        # Set up children pointers (all except the root)
        for node in self.nodes:
            if node is not self.root:
                assert node.parent is not None
                node.parent.children.append(node)

        # Compute a fixed pre-order traversal to record each node's range.
        pre: list[Node] = []
        self.root.preorder(pre)

        # Build a persistent RMQ structure over the node values using the pre-order order.
        self.rmq = PersistentRMQ([node.value for node in pre])

    def __len__(self) -> int:
        return self.n

    def subtree_min(self, i: int) -> int | float:
        """Return the minimum value in the subtree rooted at node i."""
        assert 0 <= i < self.n
        node = self.nodes[i]
        return self.rmq.range_min(node.index, node.rindex)

    def update(self, i: int, v: int) -> "PersistentSMQ":
        """
        Returns a new PersistentSMQ instance where the value at node i
        is updated to v. The original SMQ remains unchanged.
        """
        assert 0 <= i < self.n

        # Create a new SMQ instance without recomputing the full tree structure.
        new_smq = PersistentSMQ.__new__(PersistentSMQ)
        new_smq.n = self.n

        # Copy the nodes list shallowly.
        # (The preorder order and indices remain unchanged.)
        new_smq.nodes = self.nodes[:]  
        new_smq.root = self.root  # tree structure stays the same

        # Create a new Node for the updated node, copying over precomputed indices.
        old_node = self.nodes[i]
        new_node = Node(
            label=old_node.label,
            value=v,
            parent=old_node.parent,
            children=old_node.children.copy(),
            index=old_node.index,
            rindex=old_node.rindex,
        )
        new_smq.nodes[i] = new_node

        # Update the RMQ persistently at the pre-order index corresponding to the updated node.
        new_smq.rmq = self.rmq.update(new_node.index, v)
        return new_smq

    def __getitem__(self, i: int) -> int:
        assert 0 <= i < self.n
        return self.nodes[i].value

if __name__ == '__main__':
    # Example initialization:
    values = [1, 4, 5, 6, 3, 5, 6, 8, 2, 4]
    # For example, assume node 0 is the root, and the parent pointer array is given.
    # (Make sure the parent array defines a valid tree structure.)
    parent = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]  # Example parent relationships
    smq = PersistentSMQ(values, root=0, parent=parent)

    print("Original SMQ:")
    # For example, get the subtree minimum for node 1.
    print("Subtree min at node 1:", smq.subtree_min(1))
    print("Value at node 8:", smq[8])

    # Create a new version with an update. (For instance, update node 2's value to 12.)
    smq2 = smq.update(8, 1)

    print("\nAfter update (node 8 = 1):")
    print("New value at node 2:", smq2[8])
    print("New subtree min at node 1:", smq2.subtree_min(1))

    # The original SMQ remains unchanged:
    print("\nOriginal SMQ remains unchanged:")
    print("Original value at node 2:", smq[2])