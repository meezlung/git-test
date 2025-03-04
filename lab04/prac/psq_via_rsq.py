# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import product
from math import inf

from rsq_segtree import RSQ

@dataclass
class Edge:
    i: int
    j: int

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
            i = self.nodes[edge.i - 1]
            j = self.nodes[edge.j - 1]
            i.children.append(j)
            j.children.append(i)

        # root arbitrarily
        self.root = self.nodes[0]

        # preorder
        pre = self.root.preorder1()

        # preorder again
        pre = self.root.preorder2()

        # initialize RMQ on preorder
        print([node.value for node in pre])
        self.rsq = RSQ([node.value for node in pre])

        super().__init__()


    def __len__(self):
        return self.n


    def path_sum_special(self, i: Node, j: Node):
        assert i.in_same_path(j)
        if i.index > j.index:
            i, j = j, i
        return self.rsq.range_sum(i.index, j.index + 1)


    def path_sum(self, _i: int, _j: int):
        """sum of values in the path from i to j"""
        assert all(0 <= k < len(self) for k in (_i, _j))
        i = self.nodes[_i]
        j = self.nodes[_j]

        ans = 0

        while not i.in_same_path(j):
            if i.topmost.depth > j.topmost.depth:
                # climb i
                ans += self.path_sum_special(i, i.topmost)
                i = i.topmost.parent
            else:
                # climb j
                ans += self.path_sum_special(j.topmost, j)
                j = j.topmost.parent

        ans += self.path_sum_special(i, j)

        return ans


    def __getitem__(self, i: int) -> int:
        assert 0 <= i < len(self)
        node = self.nodes[i]
        return node.value

    def __setitem__(self, i: int, v: int) -> None:
        """set the value at i to v"""
        assert 0 <= i < len(self)
        node = self.nodes[i]
        node.value = v
        self.rsq[node.index] = v


def offline_pmq(values: Sequence[int], edges: Sequence[Edge], queries: Sequence[tuple[int, int]]):
    # just solve offline PMQ online
    pmq = PMQ(values, edges)
    return [pmq.path_sum(i, j) for i, j in queries]


if __name__ == '__main__':
    values = [1, 1, 1, 0, 0]
    edges = [
        Edge(1, 2), 
        Edge(1, 3), 
        Edge(1, 4), 
        Edge(1, 5)
    ]
    queries = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 2)]

    print(offline_pmq(values, edges, queries))