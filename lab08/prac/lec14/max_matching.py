# type: ignore

def max_matching(n: int, m: int, edges: tuple[tuple[int, int]]):
    
    adj: list[list[int]] = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)

    to_left = [-1] * m
    def augment(i: int):
        if not vis[i]:
            vis[i] = True
            for j in adj[i]:
                if to_left[j] == -1 or augment(to_left[j]):
                    to_left[j] = i
                    return True
                
        return False
    
    ans = 0
    for i in range(n):
        vis = [False] * n
        if augment(i):
            ans += 1

    return ans, to_left

def bipartite_matching(n, m, edges):
    """
    Computes the maximum matching in a bipartite graph.
    
    Returns:
      match_count: Size of maximum matching.
      to_left: Array of length m where to_left[j] = matched left vertex for right vertex j (or -1).
      to_right: Array of length n where to_right[i] = matched right vertex for left vertex i (or -1).
      adj: The adjacency list for the left side.
    """
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
    
    to_left = [-1] * m
    to_right = [-1] * n

    def augment(u, visited):
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                if to_left[v] == -1 or augment(to_left[v], visited):
                    to_left[v] = u
                    to_right[u] = v
                    return True
        return False

    match_count = 0
    for u in range(n):
        visited = [False] * m
        if augment(u, visited):
            match_count += 1

    return match_count, to_left, to_right, adj


def min_vertex_cover(n, m, edges):
    """
    Computes the minimum vertex cover for a bipartite graph using the maximum matching.
    
    Returns:
      left_cover: List of left vertices to include.
      right_cover: List of right vertices to include.
      
    The algorithm follows these steps:
      1. Compute a maximum matching.
      2. From each unmatched left vertex, run a DFS along alternating paths.
      3. The minimum vertex cover is: 
            (Left vertices NOT visited) U (Right vertices visited)
    """
    match_count, to_left, to_right, adj = bipartite_matching(n, m, edges)
    
    left_visited = [False] * n
    right_visited = [False] * m

    def dfs(u):
        left_visited[u] = True
        for v in adj[u]:
            if not right_visited[v]:
                # Only traverse if the edge is not the matching edge for u
                if to_right[u] != v:
                    right_visited[v] = True
                    # If v is matched, follow the matching edge back to left side
                    if to_left[v] != -1 and not left_visited[to_left[v]]:
                        dfs(to_left[v])
    
    # Start DFS from all unmatched left vertices
    for u in range(n):
        if to_right[u] == -1:
            dfs(u)

    # According to Kőnig’s theorem:
    # Left cover: vertices in left that are NOT visited.
    # Right cover: vertices in right that ARE visited.
    left_cover = [u for u in range(n) if not left_visited[u]]
    right_cover = [v for v in range(m) if right_visited[v]]
    
    return left_cover, right_cover


def min_edge_cover(n, m, edges):
    """
    Computes a minimum edge cover for a bipartite graph.
    
    Returns:
      cover_edges: List of edges (u, v) that form a minimum edge cover.
    
    Approach:
      1. Compute a maximum matching.
      2. Initialize the cover with all matching edges.
      3. For every unmatched left vertex, add an arbitrary edge from it.
      4. For every unmatched right vertex, add an arbitrary edge incident to it.
    
    Note:
      - If the graph has isolated vertices (with no incident edges),
        they cannot be covered by any edge. We assume each vertex has at least one edge.
    """
    match_count, to_left, to_right, adj = bipartite_matching(n, m, edges)
    cover_edges = set()

    # Start with all matching edges.
    for u in range(n):
        if to_right[u] != -1:
            cover_edges.add((u, to_right[u]))

    # Cover unmatched left vertices by picking any incident edge.
    for u in range(n):
        if to_right[u] == -1:
            if adj[u]:
                cover_edges.add((u, adj[u][0]))
            else:
                # u is isolated; cannot be covered by an edge.
                pass

    # Build reverse adjacency for right vertices.
    rev_adj = [[] for _ in range(m)]
    for u in range(n):
        for v in adj[u]:
            rev_adj[v].append(u)

    # Cover unmatched right vertices by picking any incident edge.
    for v in range(m):
        if to_left[v] == -1:
            if rev_adj[v]:
                cover_edges.add((rev_adj[v][0], v))
            else:
                # v is isolated; cannot be covered.
                pass

    return list(cover_edges)

def is_perfect_matching(n, m, edges):
    _, _, to_right, _ = bipartite_matching(n, m, edges)
    return all(match != -1 for match in to_right)

def is_bipartite_dfs(graph):
    color = {}
    
    def dfs(u, c):
        color[u] = c
        for v in graph[u]:
            if v not in color:
                if not dfs(v, 1 - c):
                    return False
            elif color[v] == color[u]:
                return False
        return True
    
    for vertex in graph:
        if vertex not in color:
            if not dfs(vertex, 0):
                return False
    return True

print("Is graph bipartite (DFS)?", is_bipartite_dfs(graph))

if __name__ == '__main__':
    edges = (
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 1),
    )
    n, m = 5, 4

    match_count, to_left, to_right, _ = bipartite_matching(n, m, edges)
    print("Maximum matching size:", match_count)
    print("Matching from right side (to_left):", to_left)
    print("Matching from left side (to_right):", to_right)
    
    left_cover, right_cover = min_vertex_cover(n, m, edges)
    print("Minimum vertex cover:")
    print("  Left vertices:", left_cover)
    print("  Right vertices:", right_cover)
    
    print("Is perfect matching (for left side)?", is_perfect_matching(n, m, edges))


if __name__ == '__main__':
    print(max_matching(5, 4, ( # type: ignore
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 1),
    )))