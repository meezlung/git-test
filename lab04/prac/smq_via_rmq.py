""" Subtree Minimum Query """
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

        self.l_index = len(pre) # left index

        pre.append(self)
        for child in self.children:
            child.preorder(pre)
        
        self.r_index = len(pre) # right index


class SMQ(Generic[T]):
    def __init__(self, labels: Sequence[T], values: Sequence[int], root: int, parent: Sequence[int]):
        self.n = len(values)
        self.nodes = [Node(label=labels[i], value=values[i]) for i in range(self.n)]

        # initialize the root
        self.root = self.nodes[root]

        # initialize parents
        for i in range(self.n):
            self.nodes[i].parent = self.nodes[parent[i]]

        # initialize children
        for i in self.nodes:
            if i is not self.root and i.parent is not None:
                i.parent.children.append(i)

        # preorder traversal
        pre: list[Node[T]] = []
        self.root.preorder(pre)

        pprint(pre)

        self.rmq = RMQ([node.value for node in pre])
        
    def __len__(self):
        return self.n
    
    def subtree_min(self, i: int):
        # min of the values rooted at i
        assert 0 <= i < len(self)
        node = self.nodes[i]
        return self.rmq.range_min(node.l_index, node.r_index)
    
    def __setitem__(self, i: int, v: int, l: T):
        # set the value at i to v, and the label at i to l
        assert 0 <= i < len(self)
        node = self.nodes[i]
        node.value = v
        node.label = l
        self.rmq[node.l_index] = v


if __name__ == '__main__':
    labels: Sequence[str] = ['A', 'B', 'C', 'D']
    values: Sequence[int] = [42, 21, 69, 12]
    root: int = 0
    parent: Sequence[int] = [0, 0, 0, 2]

    smq = SMQ(labels, values, root, parent)
    print(smq.subtree_min(0))
    print(smq.subtree_min(1))
    print(smq.subtree_min(2))
    print(smq.subtree_min(3))