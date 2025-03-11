# type: ignore
from collections import deque, defaultdict
from collections.abc import Sequence

Path = tuple[int, int]

def num_trips(paths: Sequence[Path], k: int) -> list[int]:
    # Build adjacency list
    adj = defaultdict(list)
    nodes = set()
    for u, v in paths:
        adj[u].append(v)
        adj[v].append(u)
        nodes.add(u)
        nodes.add(v)
    c = max(nodes) if nodes else 1  # handle empty paths case
    
    result = []
    for j in range(1, c + 1):
        # BFS to get distances and parents
        distance = {}
        parent = {}
        q = deque()
        q.append(j)
        distance[j] = 0
        parent[j] = None
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in distance:
                    distance[v] = distance[u] + 1
                    parent[v] = u
                    q.append(v)
        
        # Compute child_j for each node
        child_j = {}
        # Process nodes in BFS order to ensure parents are processed first
        processed = set([j])
        child_j[j] = None  # j's child is not in any subtree
        q = deque([j])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in processed and parent.get(v, None) == u:
                    if u == j:
                        child_j[v] = v
                    else:
                        child_j[v] = child_j[u]
                    processed.add(v)
                    q.append(v)
        
        # Group nodes into subtrees (excluding j itself)
        subtrees = defaultdict(list)
        for u in range(1, c + 1):
            if u == j:
                continue
            subtree = child_j.get(u, None)
            if subtree is not None and subtree in child_j.values():
                subtrees[subtree].append(distance[u])
        
        # Calculate sum of pairs between different subtrees
        subtree_list = list(subtrees.values())
        sum_pairs = 0
        for i in range(len(subtree_list)):
            for j_sub in range(i + 1, len(subtree_list)):
                a = sorted(subtree_list[i])
                b = sorted(subtree_list[j_sub])
                ptr = len(b) - 1
                count = 0
                for d_a in a:
                    while ptr >= 0 and d_a + b[ptr] > k:
                        ptr -= 1
                    if ptr >= 0:
                        count += ptr + 1
                sum_pairs += count
        
        # Calculate count of nodes with distance <=k including j
        cnt = sum(1 for u in range(1, c + 1) if u in distance and distance[u] <= k)
        
        result.append(sum_pairs + cnt)
    
    return result