# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import product
from math import inf

from rmq_segtree import RMQ

@dataclass
class Edge:
    i: int
    j: int

@dataclass
class Node:
    label: int
    value: int
    adj: "list[Node]" = field(default_factory=list)
    parent: "Node | None" = None
    depth: int = 0
    size: int = 0
    min_to_root: int = 0
    child_root: "Node | None" = None
    queries: "list[Query]" = field(default_factory=list)


    def preorder(self):
        self.parent = self
        self.depth = 0
        self.min_to_root = self.value
        self.child_root = self
        pre = []
        self._preorder(pre)
        return pre


    def _preorder(self, pre):
        pre.append(self)
        self.size = 1
        for child in self.adj:
            if child is not self.parent:  # do not go back up the parent!
                child.parent = self
                child.depth = self.depth + 1
                child.min_to_root = min(child.value, self.min_to_root)
                child.child_root = child if child.depth <= 1 else self.child_root
                child._preorder(pre)
                self.size += child.size


    def in_same_subtree(self, other):
        return self.child_root is other.child_root


    def find_centroid(self):
        pre = self.preorder()

        while pre[-1].size * 2 < self.size:
            pre.pop()

        return pre[-1]


    def answer_queries(self, queries):
        # root to centroid
        # without this, it will still work, but worst case is quadratic
        self = self.find_centroid()
        
        pre = self.preorder()

        for child in self.adj:
            child.queries = []

        # answer queries going through the root
        for query in queries:
            if query.i.in_same_subtree(query.j) and (query.i is not self):
                # answer 'query' later
                query.i.child_root.queries.append(query)
            else:
                query.ans = min(query.i.min_to_root, query.j.min_to_root)

        # answer queries not going through the root
        for child in self.adj:

            # remove pointer to root
            child.adj.remove(self)

            # recurse
            child.answer_queries(child.queries)


@dataclass
class Query:
    i: Node
    j: Node
    index: int
    ans: int = 0


def offline_pmq(values: Sequence[int], edges: Sequence[Edge], queries: Sequence[tuple[int, int]]):
    # make node objects
    nodes = [Node(i, value=value) for i, value in enumerate(values)]

    # make query objects
    qs = [Query(i=nodes[i], j=nodes[j], index=idx) for idx, (i, j) in enumerate(queries)]

    # make adjacency lists
    for edge in edges:
        i = nodes[edge.i]
        j = nodes[edge.j]

        # add to both directions
        i.adj.append(j)
        j.adj.append(i)

    # root arbitrarily
    root = nodes[0]

    # answer queries
    root.answer_queries(qs)

    # save answers to array in the right order
    ans = [None]*len(qs)
    for query in qs:
        assert ans[query.index] is None
        ans[query.index] = query.ans

    return ans
