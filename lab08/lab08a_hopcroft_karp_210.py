# type: ignore

from collections import deque

def hopcroft_karp(n, m, adj):
    INF = float('inf')
    dist = [INF] * n
    matching_left = [-1] * n
    matching_right = [-1] * m

    def bfs():
        queue = deque()
        for u in range(n):
            if matching_left[u] == -1:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = INF
        distance = INF
        while queue:
            u = queue.popleft()
            if dist[u] < distance:
                for v in adj[u]:
                    # If v is unmatched, we found a free node at the next layer.
                    if matching_right[v] == -1:
                        distance = dist[u] + 1
                    else:
                        # Otherwise, try to set the distance for the node matched with v.
                        if dist[matching_right[v]] == INF:
                            dist[matching_right[v]] = dist[u] + 1
                            queue.append(matching_right[v])
        return distance != INF

    def dfs(u, distance):
        if dist[u] < distance:
            for v in adj[u]:
                # Either v is free, or we can continue along an augmenting path.
                if matching_right[v] == -1 or (dist[matching_right[v]] == dist[u] + 1 and dfs(matching_right[v], distance)):
                    matching_left[u] = v
                    matching_right[v] = u
                    return True
            dist[u] = INF
            return False
        return True

    matching = 0
    while bfs():
        for u in range(n):
            if matching_left[u] == -1 and dfs(u, INF):
                matching += 1

    return matching, matching_left, matching_right


def choose_faces(dice):
    d = len(dice)
    # Compute overall maximum face value.
    max_all = max(face for die in dice for face in die)
    
    # Try candidate starting values C from 1 to max_all - d + 1.
    for C in range(1, max_all - d + 2):
        # Build the bipartite graph.
        # Left nodes: dice indices 0..d-1.
        # Right nodes: positions 0..d-1 corresponding to numbers C, C+1, ..., C+d-1.
        # We'll build an adjacency list for left nodes.
        adj = [[] for _ in range(d)]
        mapping = {}  # (die index, position) -> face index (1-indexed)
        
        for i, die in enumerate(dice):
            for face_index, face_val in enumerate(die, start=1):
                p = face_val - C
                if 0 <= p < d:
                    # We add an edge from die i to position p.
                    if p not in adj[i]:
                        adj[i].append(p)
                        mapping[(i, p)] = face_index
        
        # Run Hopcroft-Karp on the bipartite graph with d left nodes and d right nodes.
        match_count, matching_left, _ = hopcroft_karp(d, d, adj)
        if match_count == d:
            # Recover the face choices for each die.
            result = [None] * d
            for i in range(d):
                p = matching_left[i]
                result[i] = mapping[(i, p)]
            return result

    # Since a valid solution is guaranteed, we should never reach here.
    return []
