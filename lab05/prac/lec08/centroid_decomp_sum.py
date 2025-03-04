
from collections.abc import Sequence
from dataclasses import dataclass, field

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
    sum_to_root: int = 0
    child_root: "Node | None" = None
    queries: "list[Query]" = field(default_factory=list)

    def preorder(self):
        self.parent = self
        self.depth = 0
        self.sum_to_root = self.value
        self.child_root = self
        pre: "list[Node]" = []
        self._preorder(pre)
        return pre
    
    def _preorder(self, pre: "list[Node]"):
        pre.append(self)
        self.size = 1

        for child in self.adj:
            if child is not self.parent: # do not go back to parent
                child.parent = self
                child.depth = self.depth + 1
                child.sum_to_root = child.value + self.sum_to_root
                child.child_root = child if child.depth <= 1 else self.child_root
                child._preorder(pre)
                self.size += child.size

    def in_same_subtree(self, other: "Node"):
        return self.child_root is other.child_root

    def find_centroid(self):
        pre: "list[Node]" = self.preorder()

        while pre[-1].size * 2 < self.size:
            pre.pop()

        return pre[-1]
    
    def answer_queries(self, queries: "list[Query]"):
        # root to centroid
        self = self.find_centroid() # this can still work without this, but worse case is quadratic

        _ = self.preorder() # preorder again from the centroid

        for child in self.adj:
            child.queries = []

        # answer queries going through the root
        for query in queries:
            if query.i.in_same_subtree(query.j) and (query.i is not self):
                # answer query later
                assert query.i.child_root is not None
                query.i.child_root.queries.append(query)
            
            else:
                # can be answered agad
                query.ans = query.i.sum_to_root + query.j.sum_to_root - self.value

        # answer queries not going through the root
        for child in self.adj:
            
            # remove pointer to the root
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
    nodes = [Node(label=i, value=value) for i, value in enumerate(values)]

    # make query objects
    qs = [Query(i=nodes[i], j=nodes[j], index=idx) for idx, (i, j) in enumerate(queries)]

    # make adj list
    for edge in edges:
        i = nodes[edge.j]
        j = nodes[edge.i]

        # add to both directions
        i.adj.append(j)
        j.adj.append(i)
    
    # root arbitrarily
    root = nodes[0]

    # answer queries
    root.answer_queries(qs)

    # save answers to array in the right order
    ans: list[int | None] = [None] * len(qs)
    for query in qs:
        assert ans[query.index] is None
        ans[query.index] = query.ans

    return ans


if __name__ == '__main__':
    values = [1, 2, 3, 4, 5]
    edges = [
        Edge(0, 1), 
        Edge(0, 2), 
        Edge(1, 3), 
        Edge(1, 4)
    ]
    queries = [(0, 3), (2, 4), (1, 4), (0, 1), (1, 2), (2, 3), (3, 4)]

    print(offline_pmq(values, edges, queries))

    values2 = [69, 420]
    edges2 = [
        Edge(0, 1),
    ]
    queries2 = [(0, 0), (0, 1)]

    print(offline_pmq(values2, edges2, queries2))