from collections.abc import Sequence

Line = tuple[tuple[int, int], int]

class UnionFind:
    def __init__(self, nodes: list[int]):
        self.parent = {node: node for node in nodes}
        self.weight = {node: 1 for node in nodes}

    def find(self, i: int):
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])
            return self.parent[i]
    
    def union(self, i: int, j: int) -> bool:
        i_parent = self.find(i)
        j_parent = self.find(j)

        if i_parent == j_parent:
            return False
        
        # always make j_parent weight bigger
        if self.weight[i_parent] > self.weight[j_parent]:
            i_parent, j_parent = j_parent, i_parent

        assert self.weight[i_parent] <= self.weight[j_parent]

        self.parent[i_parent] = j_parent
        self.weight[j_parent] += self.weight[i_parent]

        return True

def max_tracks(n: int, lines: Sequence[Line]) -> tuple[int, list[int]]:
    sorted_lines = sorted(lines, key=lambda x: x[1])

    idx = {lines[i]: i + 1 for i in range(len(lines))}

    nodes: list[int] = [i for i in range(1, n + 1)]

    uf = UnionFind(nodes)

    mst: list[Line] = []
    free: list[int] = []
    free_tracks_num = 0

    for (u, v), w in sorted_lines:
        if uf.union(u, v):
            mst.append(((u, v), w))
        else:
            free.append(idx[(u, v), w])
            free_tracks_num += w

    return (free_tracks_num, free)