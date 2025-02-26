

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TypeVar, Generic
from rmq_segtree import RMQ
from pprint import pprint

T = TypeVar("T")

@dataclass
class Node(Generic[T]):
    label: T
    value: int
    parent: "Node[T] | None" = None
    children: "list[Node[T]]" = field(default_factory=list)
    l_index: int = -1
    r_index: int = -1

    def preorder(self, pre: "list[Node[T]]"):
        self.l_index = len(pre)
        pre.append(self)
        for child in self.children:
            child.preorder(pre)
        self.r_index = len(pre)

class SMQ(Generic[T]):
    def __init__(self, nodes: "Sequence[tuple[T, int]]", edges: "Sequence[tuple[int, int]]"):
        self.n = len(nodes)
        self.nodes = [Node(label=label, value=value) for label, value in nodes]

        # initialize parent-child relationships
        for parent, child in edges:
            self.nodes[child].parent = self.nodes[parent]
            self.nodes[parent].children.append(self.nodes[child])

        # find root (node with no parent)
        self.root = next(node for node in self.nodes if node.parent is None)

        # preorder traversal
        pre: list[Node[T]] = []
        self.root.preorder(pre)

        pprint(pre)

        self.rmq = RMQ([node.value for node in pre])

    def __len__(self):
        return self.n
    
    def subtree_min(self, i: int):
        assert 0 <= i < len(self)
        node = self.nodes[i]
        return self.rmq.range_min(node.l_index, node.r_index)
    
    def __setitem__(self, i: int, v: int, l: T):
        assert 0 <= i < len(self)
        node = self.nodes[i]
        node.value = v
        node.label = l
        self.rmq[node.l_index] = v

if __name__ == '__main__':
    nodes = [('A', 42), ('B', 21), ('C', 69), ('D', 12)]
    edges = [(0, 1), (0, 2), (2, 3)]
    
    smq = SMQ(nodes, edges)
    print(smq.subtree_min(0))
    print(smq.subtree_min(1))
    print(smq.subtree_min(2))
    print(smq.subtree_min(3))
