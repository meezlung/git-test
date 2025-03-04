# type: ignore

class InfArray:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left or self
        self.right = right or self
        super().__init__()

    def __getitem__(self, i):
        if i == 0:
            return self.value
        elif i % 2 != 0:
            return self.left[(i - 1) // 2]
        else:
            # i is even
            return self.right[(i - 1) // 2]

    def assign(self, i, v):
        if i == 0:
            return InfArray(value=v, left=self.left, right=self.right)
        elif i % 2 != 0:
            return InfArray(value=self.value, left=self.left.assign((i - 1) // 2, v), right=self.right)
        else:
            return InfArray(value=self.value, left=self.left, right=self.right.assign((i - 1) // 2, v))


class PersistentUnionFindInfinite:
    def __init__(self, parent, rank):
        self.parent = parent  # InfArray for parent pointers
        self.rank = rank      # InfArray for ranks

    @classmethod
    def initialize(cls):
        """
        Initializes the infinite union-find.
        The parent's array is initialized with default value None, meaning that if no value
        is stored for index i, then by default parent[i] = i.
        The rank array is initialized to 0 everywhere.
        """
        # parent's default is None; rank default is 0.
        parent = InfArray(value=None)
        rank = InfArray(value=0)
        return cls(parent, rank)

    def get_parent(self, i):
        """
        Returns the stored parent for index i.
        If no update was made (i.e. parent's value is None), then the default is that i is its own parent.
        """
        p = self.parent[i]
        return i if p is None else p

    def get_rank(self, i):
        """
        Returns the rank for index i. (Default is 0.)
        """
        r = self.rank[i]
        return 0 if r is None else r

    def find(self, i):
        """
        Finds the representative (root) of the set containing i.
        This implementation does not perform path compression.
        Running time is O(log i) (proportional to the cost of InfArray lookups).
        """
        p = self.get_parent(i)
        if p == i:
            return i
        else:
            return self.find(p)

    def union(self, i, j):
        """
        Unites the sets containing i and j and returns a new persistent union–find structure.
        Running time is O(log i + log j) for the InfArray assignments.
        """
        r_i = self.find(i)
        r_j = self.find(j)
        if r_i == r_j:
            return self  # already in the same set

        rank_i = self.get_rank(r_i)
        rank_j = self.get_rank(r_j)
        new_parent = self.parent
        new_rank = self.rank

        if rank_i < rank_j:
            new_parent = new_parent.assign(r_i, r_j)
        elif rank_i > rank_j:
            new_parent = new_parent.assign(r_j, r_i)
        else:
            new_parent = new_parent.assign(r_j, r_i)
            new_rank = new_rank.assign(r_i, rank_i + 1)
        return PersistentUnionFindInfinite(new_parent, new_rank)


# Example usage
if __name__ == '__main__':
    versions = []  # List to store versions of union-find.
    
    # Start with the initial version.
    uf0 = PersistentUnionFindInfinite.initialize()
    versions.append(uf0)
    
    # Perform some unions; each union returns a new version.
    uf1 = uf0.union(100, 200)
    versions.append(uf1)
    
    uf2 = uf1.union(50, 100)
    versions.append(uf2)
    
    uf3 = uf2.union(300, 400)
    versions.append(uf3)
    
    # Now we have several versions:
    # Version 0: initial, no unions.
    # Version 1: union(100, 200)
    # Version 2: union(50, 100) => now 50, 100, 200 in one set.
    # Version 3: union(300, 400)
    
    print("Version 0: find(100) =", uf0.find(100))  # 100 is alone (represents itself)
    print("Version 1: find(100) =", uf1.find(100))  # 100 and 200 united.
    print("Version 1: find(200) =", uf1.find(200))
    print("Version 2: find(50) =", uf2.find(50))    # 50, 100, 200 united.
    print("Version 2: find(200) =", uf2.find(200))
    print("Version 3: find(300) =", uf3.find(300))  # 300 and 400 united.
    print("Version 3: find(400) =", uf3.find(400))
    
    # You can still refer back to older versions:
    print("Version 0 (old version) remains unchanged: find(100) =", versions[0].find(100))