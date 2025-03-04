# type: ignore

###############################################################################
# Part 1: Persistent Array (for finite union–find)
###############################################################################

class Node:
    __slots__ = ('left', 'right', 'val')
    def __init__(self, left, right, val):
        self.left = left
        self.right = right
        self.val = val

class PersistentArray:
    def __init__(self, root, n):
        self.root = root
        self.n = n

    @staticmethod
    def build(arr, l, r):
        """Builds a persistent tree for indices [l, r)."""
        if r - l == 1:
            return Node(None, None, arr[l])
        mid = (l + r) // 2
        left_node = PersistentArray.build(arr, l, mid)
        right_node = PersistentArray.build(arr, mid, r)
        # The internal node's value is not used.
        return Node(left_node, right_node, None)

    @classmethod
    def from_list(cls, arr):
        root = PersistentArray.build(arr, 0, len(arr))
        return cls(root, len(arr))

    def query(self, index):
        """Returns the value at a given index in O(log n) time."""
        def _query(node, l, r, index):
            if r - l == 1:
                return node.val
            mid = (l + r) // 2
            if index < mid:
                return _query(node.left, l, mid, index)
            else:
                return _query(node.right, mid, r, index)
        return _query(self.root, 0, self.n, index)

    def update(self, index, value):
        """Returns a new PersistentArray with index updated to value."""
        def _update(node, l, r):
            if r - l == 1:
                return Node(None, None, value)
            mid = (l + r) // 2
            if index < mid:
                new_left = _update(node.left, l, mid)
                return Node(new_left, node.right, None)
            else:
                new_right = _update(node.right, mid, r)
                return Node(node.left, new_right, None)
        new_root = _update(self.root, 0, self.n)
        return PersistentArray(new_root, self.n)

###############################################################################
# Finite Persistent Union–Find on [0, n-1]
###############################################################################

class PersistentUnionFindFinite:
    def __init__(self, parent, rank):
        self.parent = parent  # PersistentArray for parent pointers
        self.rank = rank      # PersistentArray for ranks

    @classmethod
    def initialize(cls, n):
        """Initializes union–find on [0, n-1] in O(n) time."""
        parent_list = list(range(n))
        rank_list = [0] * n
        parent_pa = PersistentArray.from_list(parent_list)
        rank_pa = PersistentArray.from_list(rank_list)
        return cls(parent_pa, rank_pa)

    def find(self, i):
        """Returns the representative of i (without path compression)."""
        p = self.parent.query(i)
        if p == i:
            return i
        else:
            return self.find(p)

    def union(self, i, j):
        """Unites the sets containing i and j, returning a new persistent structure."""
        r_i = self.find(i)
        r_j = self.find(j)
        if r_i == r_j:
            return self  # Already united
        rank_i = self.rank.query(r_i)
        rank_j = self.rank.query(r_j)
        new_parent = self.parent
        new_rank = self.rank
        if rank_i < rank_j:
            new_parent = new_parent.update(r_i, r_j)
        elif rank_i > rank_j:
            new_parent = new_parent.update(r_j, r_i)
        else:
            new_parent = new_parent.update(r_j, r_i)
            new_rank = new_rank.update(r_i, rank_i + 1)
        return PersistentUnionFindFinite(new_parent, new_rank)


if __name__ == "__main__":
    # finite union find on [0, n-1]
    n = 10
    uf_finite = PersistentUnionFindFinite.initialize(n)
    uf_finite1 = uf_finite.union(2, 3)    
    uf_finite2 = uf_finite.union(3, 5)
    uf_finite3 = uf_finite.union(7, 8)

    print("Finite UF: find(2) =", uf_finite1.find(2))  # Should output representative for element 2
    print("Finite UF: find(5) =", uf_finite1.find(5))
    print("Finite UF: find(7) =", uf_finite1.find(7))

    print("Finite UF: find(2) =", uf_finite2.find(2))  # Should output representative for element 2
    print("Finite UF: find(5) =", uf_finite2.find(5))
    print("Finite UF: find(7) =", uf_finite2.find(7))

    print("Finite UF: find(2) =", uf_finite3.find(2))  # Should output representative for element 2
    print("Finite UF: find(5) =", uf_finite3.find(5))
    print("Finite UF: find(7) =", uf_finite3.find(7))
