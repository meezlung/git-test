# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass, field

@dataclass
class Node:
    label: int
    value: int
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)

    def subtree_min(self):
        # min of subtree, brute force
        res = self.value
        for child in self.children:
            res = min(res, child.subtree_min())
        return res


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

        super().__init__()


    def __len__(self) -> int:
        return self.n


    def subtree_min(self, i: int):
        """min of values in the subtree rooted at i"""
        assert 0 <= i < len(self)
        return self.nodes[i].subtree_min()


    def __setitem__(self, i: int, v: int) -> None:
        """set the value at i to v"""
        assert 0 <= i < len(self)
        self.nodes[i].value = v
