# type: ignore
from collections.abc import Sequence
from math import inf
from dataclasses import dataclass, field
class Node:
    def __init__(self, seq: Sequence[int], i: int, j: int):
        self.i = i
        self.j = j
        if self.is_leaf():
            self.min_value = seq[i]
            self.max_value = seq[i]
            self.l = self.r = None
        else:
            k = (i + j) // 2
            assert i < k < j
            self.l = Node(seq, i, k)
            self.r = Node(seq, k, j)
            self.combine()
    def is_leaf(self):
        return self.j - self.i == 1
    def combine(self):
        self.min_value = min(self.l.min_value, self.r.min_value)
        self.max_value = max(self.l.max_value, self.r.max_value)
    def set(self, i: int, v: int):
        if not self.i <= i < self.j:
            return
        if self.is_leaf():
            self.min_value = v
            self.max_value = v
        else:
            self.l.set(i, v)
            self.r.set(i, v)
            self.combine()
    def range_min_query(self, i: int, j: int) -> float:
        if i <= self.i and self.j <= j:
            return self.min_value
        elif j <= self.i or self.j <= i:
            return inf
        else:
            lmin = self.l.range_min_query(i, j)
            rmin = self.r.range_min_query(i, j)
            return min(lmin, rmin)
    def range_max_query(self, i: int, j: int) -> float:
        if i <= self.i and self.j <= j:
            return self.max_value
        elif j <= self.i or self.j <= i:
            return -inf
        else:
            lmax = self.l.range_max_query(i, j)
            rmax = self.r.range_max_query(i, j)
            return max(lmax, rmax)
        
class RMQ:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.root = Node(values, 0, self.n)
    def set(self, i: int, v: int):
        self.root.set(i, v)
    def range_min_query(self, i: int, j: int):
        return self.root.range_min_query(i, j)
    def range_max_query(self, i: int, j: int):
        return self.root.range_max_query(i, j)
    
@dataclass
class SegTreeNode:
    label: str
    value: int
    parent: "SegTreeNode | None" = None
    children: "list[SegTreeNode]" = field(default_factory=list)
    l_index: int = -1
    r_index: int = -1

    def preorder(self, pre: "list[SegTreeNode]"):
        self.l_index = len(pre)
        pre.append(self)
        for child in self.children:
            child.preorder(pre)
        self.r_index = len(pre)

class SMQ:
    def __init__(self, labels: Sequence[str], values: Sequence[int], root: int, parent: Sequence[str]):
        self.n = len(values)
        self.nodes = [SegTreeNode(label=labels[i], value=values[i]) for i in range(self.n)]
        self.node_labels = {node.label: node for node in self.nodes}
        self.root = self.nodes[root]
        for i in range(self.n):
            self.nodes[i].parent = self.node_labels[parent[i]]
        for i in self.nodes:
            if i is not self.root and i.parent is not None:
                i.parent.children.append(i)
        self.pre: list[SegTreeNode] = []
        self.root.preorder(self.pre)
        self.rmq = RMQ([node.value for node in self.pre])
    def __len__(self):
        return self.n
    def set(self, i: int, v: int):
        assert 0 <= i < len(self)
        self.rmq.set(i, v)

class MilitaryManagement:
    def __init__(self, troops: Sequence[tuple[str, str | None, int]]):
        labels = []
        values = []
        parent: dict[str, str | None] = {}
        root = 0
        for idx, (name, boss, salary) in enumerate(troops):
            labels.append(name)
            values.append(salary)
            parent[name] = boss if boss is not None else name
            root = idx if boss is None else 0
        parents = [parent[label] for label in labels]
        self.smq = SMQ(labels, values, root, parents)
        super().__init__()
    def update_salary(self, t: str, v: int) -> None:
        idx = self.smq.node_labels[t].l_index 
        self.smq.set(idx, v)
    def get_salary_range(self, t: str) -> tuple[int, int]:
        node = self.smq.node_labels[t]
        return (
            self.smq.rmq.range_min_query(node.l_index, node.r_index),
            self.smq.rmq.range_max_query(node.l_index, node.r_index)
        )