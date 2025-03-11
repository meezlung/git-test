# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class Node:
    label: int
    parent: "Node | None" = None
    depth: int = 0
    children: "list[Node]" = field(default_factory=list)
    teleport: "Node | None" = None
    teleport2: "Node | None" = None


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

        self.a = int(n**(1/3)) + 1
        self.a2 = int(n**(2/3)) + 1

        anc = []
        def dfs(i):

            # initialize teleports of size a and a2
            i.teleport = anc[-self.a] if len(anc) >= self.a else root
            i.teleport2 = anc[-self.a2] if len(anc) >= self.a2 else root

            anc.append(i)
            for j in i.children:
                j.depth = i.depth + 1
                dfs(j)
            anc.pop()

        dfs(root)


        super().__init__()






    def climb(self, i, d):
        while i.depth >= d + self.a2:
            i = i.teleport2

        while i.depth >= d + self.a:
            i = i.teleport

        while i.depth > d:
            i = i.parent

        return i

    def _lca(self, i, j):
        i = self.climb(i, j.depth)
        j = self.climb(j, i.depth)

        assert i.depth == j.depth

        while i.teleport2 is not j.teleport2:
            i = i.teleport2
            j = j.teleport2

        while i.teleport is not j.teleport:
            i = i.teleport
            j = j.teleport

        while i is not j:
            i = i.parent
            j = j.parent

        assert i is j

        return i




    def lca(self, i, j):
        return self._lca(self.nodes[i], self.nodes[j]).label




if __name__ == '__main__':
    tree = RootedTree([5, 2, 5, 0, 0, 5], 5)

    print(tree.lca(2, 3))
    print(tree.lca(3, 4))
    print(tree.lca(3, 0))
