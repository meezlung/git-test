# type: ignore

def max_matching(n: int, m: int, edges: list[tuple[int, int]]):
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
    to_left = [-1] * m
    def augment(u: int, visited: list[bool]):
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                if to_left[v] == -1 or augment(to_left[v], visited):
                    to_left[v] = u
                    return True
        return False
    match_count = 0
    for u in range(n):
        visited = [False] * m
        if augment(u, visited):
            match_count += 1
    return match_count
def min_shells(grid: str) -> int:
    new_grid = grid.splitlines()
    n = len(new_grid)
    edges = []
    for r in range(n):
        for c in range(n):
            if new_grid[r][c] == "#":
                edges.append((r, c))
    return max_matching(n, n, edges)