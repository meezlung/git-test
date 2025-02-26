# type: ignore

import sys
from collections import defaultdict

sys.setrecursionlimit(300000)

class CentroidDecomposition:
    def __init__(self, n):
        self.n = n
        self.graph = defaultdict(list)
        self.subtree_size = [0] * (n + 1)
        self.visited = [False] * (n + 1)
        self.k1 = 0
        self.k2 = 0
        self.ans = 0

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def compute_subtree_size(self, node, parent):
        """Compute subtree sizes for centroid selection"""
        self.subtree_size[node] = 1
        for neighbor in self.graph[node]:
            if neighbor != parent and not self.visited[neighbor]:
                self.subtree_size[node] += self.compute_subtree_size(neighbor, node)
        return self.subtree_size[node]

    def find_centroid(self, node, parent, total_size):
        """Find the centroid of the current tree"""
        for neighbor in self.graph[node]:
            if neighbor != parent and not self.visited[neighbor]:
                if self.subtree_size[neighbor] > total_size // 2:
                    return self.find_centroid(neighbor, node, total_size)
        return node

    def count_paths_from(self, node, parent, depth, distances):
        """DFS to collect path lengths from the centroid"""
        if depth > self.k2:
            return  # Ignore paths longer than k2
        distances.append(depth)
        for neighbor in self.graph[node]:
            if neighbor != parent and not self.visited[neighbor]:
                self.count_paths_from(neighbor, node, depth + 1, distances)

    def count_valid_paths(self, distances):
        """Count valid paths in the range [k1, k2] using a hash map"""
        count_map = defaultdict(int)
        count_map[0] = 1  # Path of length 0 at the centroid itself

        for d in distances:
            for length in range(self.k1, self.k2 + 1):
                if length - d in count_map:
                    self.ans += count_map[length - d]
            count_map[d] += 1

    def solve_centroid(self, root):
        """Solves the problem using centroid decomposition"""
        # Step 1: Find the centroid
        total_size = self.compute_subtree_size(root, -1)
        centroid = self.find_centroid(root, -1, total_size)
        self.visited[centroid] = True

        # Step 2: Count paths that start at the centroid
        path_distances = []  # Store all subtree distances

        for neighbor in self.graph[centroid]:
            if not self.visited[neighbor]:
                subtree_distances = []
                self.count_paths_from(neighbor, centroid, 1, subtree_distances)
                self.count_valid_paths(subtree_distances)
                path_distances.extend(subtree_distances)

        # Step 3: Recursively solve for smaller trees
        for neighbor in self.graph[centroid]:
            if not self.visited[neighbor]:
                self.solve_centroid(neighbor)

    def find_paths(self, k1, k2):
        """Entry function to compute number of paths of length in range [k1, k2]"""
        self.k1, self.k2 = k1, k2
        self.solve_centroid(1)
        print(self.ans)

def main():
    # Read input
    n, k1, k2 = map(int, sys.stdin.readline().split())
    tree = CentroidDecomposition(n)

    for _ in range(n - 1):
        a, b = map(int, sys.stdin.readline().split())
        tree.add_edge(a, b)

    # Solve using centroid decomposition
    tree.find_paths(k1, k2)

if __name__ == '__main__':
    main()