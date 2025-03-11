# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass, field

from rmq_segtree import RMQ
# from rmq_brute import RMQ
# from rmq_sqrt import RMQ


@dataclass
class Node:
    label: int
    value: int
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)
    index: int = -1
    rindex: int = -1

    def preorder(self, pre: "list[Node]"):

        self.index = len(pre)  # left index

        pre.append(self)
        for child in self.children:
            child.preorder(pre)

        self.rindex = len(pre)  # right index


class SMQ:
    def __init__(self, values: Sequence[int], root: int, parent: Sequence[int]):
        self.n = len(values)
        self.nodes = [Node(label=i, value=values[i]) for i in range(self.n)]

        # initialize root
        self.root = self.nodes[root]

        # initialize parent
        for i in range(self.n):
            self.nodes[i].parent = self.nodes[parent[i]]

        # initialize children
        for i in self.nodes:
            if i is not self.root:
                i.parent.children.append(i)

        # preorder traversal
        pre: list[Node] = []
        self.root.preorder(pre)

        # initialize RMQ structure
        self.rmq = RMQ([node.value for node in pre])

        super().__init__()


    def __len__(self) -> int:
        return self.n


    def subtree_min(self, i: int):
        """min of values in the subtree rooted at i"""
        assert 0 <= i < len(self)
        node = self.nodes[i]
        return self.rmq.range_min(node.index, node.rindex)


    def __setitem__(self, i: int, v: int) -> None:
        """set the value at i to v"""
        assert 0 <= i < len(self)
        node = self.nodes[i]
        node.value = v
        self.rmq[node.index] = v
