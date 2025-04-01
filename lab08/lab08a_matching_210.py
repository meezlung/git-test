# type: ignore

def bipartite_matching(n, m, edges):
    # Build the adjacency list for left side nodes (0 to n-1)
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
    
    to_left = [-1] * m  # which left node is matched to a given right node
    to_right = [-1] * n  # which right node is matched to a given left node

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


def choose_faces(dice):
    d = len(dice)
    # Compute overall maximum face value.
    max_all = max(face for die in dice for face in die)
    
    # We'll try candidate starting values C from 1 up to max_all - d + 1.
    for C in range(1, max_all - d + 2):
        edges = []  # list of (die_index, position) edges
        mapping = {}  # mapping from (die_index, position) to chosen face index (1-indexed)
        
        # Build the bipartite graph:
        # Left side: dice indices 0 .. d-1.
        # Right side: positions 0 .. d-1 corresponding to numbers C, C+1, ..., C+d-1.
        for i, die in enumerate(dice):
            for face_index, face_val in enumerate(die, start=1):
                p = face_val - C
                if 0 <= p < d:
                    # Add an edge from die i to position p.
                    # If there are multiple faces with the same value, one is enough.
                    if (i, p) not in mapping:
                        mapping[(i, p)] = face_index
                        edges.append((i, p))
        
        # Run bipartite matching. There are d nodes on both sides.
        match_count, to_left, to_right, _ = bipartite_matching(d, d, edges)
        if match_count == d:
            result = [None] * d
            # For each die i, get its matched position p.
            for i in range(d):
                p = to_right[i]
                result[i] = mapping[(i, p)]
            return result

    # Since a solution is guaranteed, we should never reach here.
    return []

