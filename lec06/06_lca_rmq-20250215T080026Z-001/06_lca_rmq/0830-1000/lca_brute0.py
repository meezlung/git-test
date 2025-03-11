# type: ignore

# REALLY SLOW (O(n^2) per query)

from collections.abc import Sequence

class RootedTree:
    def __init__(self, parent: Sequence[int], root: int):
        n = len(parent)
        assert 0 <= root < n
        
        assert parent[root] == root
        self.root = root
        self.parent = parent
        super().__init__()


    def depth(self, i):
        d = 0
        while i != self.root:
            i = self.parent[i]
            d += 1
        return d


    def ancestors(self, i):
        ancestors = [i]
        while i != self.root:
            i = self.parent[i]
            ancestors.append(i)

        return ancestors


    def lca(self, i, j):
        return max(set(self.ancestors(i)) & set(self.ancestors(j)), key=self.depth)


if __name__ == '__main__':
    tree = RootedTree([5, 2, 5, 0, 0, 5], 5)

    print(tree.lca(2, 3))
    print(tree.lca(3, 4))
    print(tree.lca(3, 0))

