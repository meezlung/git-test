# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import product
from math import inf

from utils import Edge

from rmq_segtree import RMQ


@dataclass
class Node:
    label: int
    value: int
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)
    topmost: "Node | None" = None
    depth: int = 0
    size: int = 0
    index: int = 0

    def preorder1(self):
        self.parent = self
        self.depth = 0
        pre = []
        self._preorder1(pre)
        return pre


    def _preorder1(self, pre):
        pre.append(self)

        if not self.is_root():
            self.children.remove(self.parent)

        self.size = 1
        for child in self.children:
            child.parent = self
            child.depth = self.depth + 1
            child._preorder1(pre)
            self.size += child.size

        # swap heaviest to first
        # without this, it will still work, but worst case is quadratic (at least)
        if self.children:
            # get index of heaviest child
            i = max(range(len(self.children)), key=lambda i: self.children[i].size)

            # swap with the first position
            self.children[i], self.children[0] = self.children[0], self.children[i]


    def preorder2(self):
        pre = []
        self._preorder2(pre)
        return pre


    def _preorder2(self, pre):

        self.index = len(pre)  # position in preorder

        pre.append(self)

        # compute topmost
        self.topmost = self.parent.topmost if self.is_special() else self
        assert self.topmost is not None

        for child in self.children:
            child._preorder2(pre)


    def is_root(self):
        return self.parent is self


    def is_special(self):
        return not self.is_root() and self.parent.children[0] is self


    def in_same_path(self, other):
        return self.topmost is other.topmost


class PMQ:
    def __init__(self, values: Sequence[int], edges: Sequence[Edge]):
        self.n = len(values)

        self.nodes = [Node(i, value=values[i]) for i in range(self.n)]

        for edge in edges:
            i = self.nodes[edge.i]
            j = self.nodes[edge.j]
            i.children.append(j)
            j.children.append(i)

        # root arbitrarily
        self.root = self.nodes[0]

        # preorder
        pre = self.root.preorder1()

        # preorder again
        pre = self.root.preorder2()

        # initialize RMQ on preorder
        self.rmq = RMQ([node.value for node in pre])

        super().__init__()


    def __len__(self):
        return self.n


    def path_min_special(self, i: Node, j: Node):
        assert i.in_same_path(j)
        if i.index > j.index:
            i, j = j, i
        return self.rmq.range_min(i.index, j.index + 1)


    def path_min(self, _i: int, _j: int):
        """min of values in the path from i to j"""
        assert all(0 <= k < len(self) for k in (_i, _j))
        i = self.nodes[_i]
        j = self.nodes[_j]

        ans = inf

        while not i.in_same_path(j):
            if i.topmost.depth > j.topmost.depth:
                # climb i
                ans = min(ans, self.path_min_special(i, i.topmost))
                i = i.topmost.parent
            else:
                # climb j
                ans = min(ans, self.path_min_special(j.topmost, j))
                j = j.topmost.parent

        ans = min(ans, self.path_min_special(i, j))

        return ans


    def __setitem__(self, i: int, v: int) -> None:
        """set the value at i to v"""
        assert 0 <= i < len(self)
        node = self.nodes[i]
        node.value = v
        self.rmq[node.index] = v


def offline_pmq(values: Sequence[int], edges: Sequence[Edge], queries: Sequence[tuple[int, int]]):
    # just solve offline PMQ online
    pmq = PMQ(values, edges)
    return [pmq.path_min(i, j) for i, j in queries]
