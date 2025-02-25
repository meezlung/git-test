from collections.abc import Sequence
from dataclasses import dataclass, field

@dataclass
class Node:
    label: int
    parent: "Node | None" = None
    depth: int = 0
    children: "list[Node]" = field(default_factory=list)
    jump: "list[Node]" = field(default_factory=list)

class RootedTree:
    def __init__(self, parent: Sequence[int], _root: int):
        n = len(parent)

        assert 0 <= _root < n

        self.nodes = [Node(i) for i in range(n)]

        self.root = root = self.nodes[_root]


        for i in range(n):
            self.nodes[i].parent = self.nodes[parent[i]]

            if parent[i] != i:
                self.nodes[parent[i]].children.append(self.nodes[i])
        
        assert root.parent is root

        def dfs(i: Node):
            for j in i.children:
                j.depth = i.depth + 1
                dfs(j)

        dfs(root)

        # initialize power-of-two jump pointers
        self.h = h = n.bit_length()

        for i in self.nodes:
            assert i.parent is not None
            i.jump = [i]*h
            i.jump[0] = i.parent

        for k in range(h - 1):
            for i in self.nodes:
                i.jump[k + 1] = i.jump[k].jump[k]

    
    def climb(self, i: Node, d: int):
        for k in reversed(range(self.h)):
            if i.depth >= d + (1 << k):
                i = i.jump[k]
            
        assert i.depth <= d
        
        return i


    def _lca(self, i: Node | None, j: Node | None):
        if i is None or j is None:
            return None
        
        i = self.climb(i, j.depth)
        j = self.climb(j, i.depth)

        assert i.depth == j.depth

        for k in reversed(range(self.h)):
            if i.jump[k] is not j.jump[k]:
                i = i.jump[k]
                j = j.jump[k]

        if i is not j:
            i = i.parent
            j = j.parent

        assert i is j

        return i
    

    def lca(self, i: int, j: int):
        node = self._lca(self.nodes[i], self.nodes[j])
        return node.label if node is not None else None
    

if __name__ == "__main__":
    tree = RootedTree([5, 2, 5, 0, 0, 5], 5)

    print(tree.lca(2, 3))
    print(tree.lca(3, 4))
    print(tree.lca(3, 0))

