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
        self.k = 0
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

    def count_paths_from(self, node, parent, depth, count_map):
        """DFS to collect path lengths from the centroid"""
        if depth > self.k:
            return  # Ignore paths longer than k
        count_map[depth] += 1  # Count occurrences of this depth
        for neighbor in self.graph[node]:
            if neighbor != parent and not self.visited[neighbor]:
                self.count_paths_from(neighbor, node, depth + 1, count_map)

    def solve_centroid(self, root):
        """Solves the problem using centroid decomposition"""
        # Step 1: Find the centroid
        total_size = self.compute_subtree_size(root, -1)
        centroid = self.find_centroid(root, -1, total_size)
        self.visited[centroid] = True

        # Step 2: Count paths that start at the centroid
        path_count = defaultdict(int)  # Dictionary to store depth frequencies
        path_count[0] = 1  # Path of length 0 at centroid itself

        for neighbor in self.graph[centroid]:
            if not self.visited[neighbor]:
                sub_count_map = defaultdict(int)
                self.count_paths_from(neighbor, centroid, 1, sub_count_map)

                # Step 3: Use stored distances to count valid paths
                for dist, freq in sub_count_map.items():
                    if self.k - dist in path_count:
                        self.ans += freq * path_count[self.k - dist]

                # Merge subtree counts into global count
                for dist, freq in sub_count_map.items():
                    path_count[dist] += freq

        # Step 4: Recursively solve on the remaining tree
        for neighbor in self.graph[centroid]:
            if not self.visited[neighbor]:
                self.solve_centroid(neighbor)

    def find_paths(self, k):
        """Entry function to compute number of paths of length exactly k"""
        self.k = k
        self.solve_centroid(1)
        print(self.ans)

def main():
    # Read input
    n, k = map(int, sys.stdin.readline().split())
    tree = CentroidDecomposition(n)

    for _ in range(n - 1):
        a, b = map(int, sys.stdin.readline().split())
        tree.add_edge(a, b)

    # Solve using centroid decomposition
    tree.find_paths(k)


if __name__ == '__main__':
    main()