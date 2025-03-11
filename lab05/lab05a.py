# type: ignore
from collections.abc import Sequence

Path = tuple[int, int, int]

def total_effort(paths: Sequence[Path], k: int) -> int:
    c = len(paths) + 1  # number of cafés (nodes)
    
    if k == 1:
        return 0
    # Edge case: if k > c, no valid paths
    if k > c:
        return 0
    
    # Build adjacency list (0-based)
    graph = [[] for _ in range(c)]
    for (u, v, s) in paths:
        # Convert 1-based to 0-based
        u -= 1
        v -= 1
        graph[u].append((v, s))
        graph[v].append((u, s))
    
    # 'used' marks nodes removed from the current decomposition
    used = [False]*c
    # 'size' array to hold subtree sizes
    size = [0]*c
    
    # This will accumulate the sum of costs for all undirected paths
    total_undirected_cost = 0
    
    #-------------------------------
    # 1) Compute subtree sizes
    #-------------------------------
    def dfs_size(u, parent):
        size[u] = 1
        for (w, wcost) in graph[u]:
            if w != parent and not used[w]:
                dfs_size(w, u)
                size[u] += size[w]
    
    #-------------------------------
    # 2) Find centroid
    #-------------------------------
    def find_centroid(u, parent, comp_size):
        for (w, wcost) in graph[u]:
            if w != parent and not used[w] and size[w] > comp_size // 2:
                return find_centroid(w, u, comp_size)
        return u
    
    #-------------------------------
    # 3) DFS to collect (distE, costW)
    #-------------------------------
    def dfs_collect(u, parent, distE, costW, vec):
        """
        From a given root (the centroid), gather (distE, costW) for each node
        in the subtree. distE = number of edges from the centroid, costW = sum of weights
        from centroid to this node.
        """
        vec.append((distE, costW))
        for (w, wght) in graph[u]:
            if w != parent and not used[w]:
                dfs_collect(w, u, distE + 1, costW + wght, vec)
    
    #-------------------------------
    # 4) Centroid Decomposition
    #-------------------------------
    from collections import defaultdict
    
    def centroid_decompose(start):
        nonlocal total_undirected_cost
        
        # (a) compute sizes in this component
        dfs_size(start, -1)
        comp_size = size[start]
        
        # (b) find centroid
        ctd = find_centroid(start, -1, comp_size)
        used[ctd] = True
        
        # globalDist: distE -> [count, sumW]
        #   - "count" = how many nodes are at 'distE' edges from centroid ctd
        #   - "sumW"  = sum of path-weights from centroid ctd to those nodes
        globalDist = defaultdict(lambda: [0, 0])
        globalDist[0] = [1, 0]  # the centroid itself: distE=0 => 1 node, sumW=0
        
        # (c) process each subtree of 'ctd'
        for (nx, edgeW) in graph[ctd]:
            if not used[nx]:
                # Collect local distances from 'ctd'
                localVec = []
                dfs_collect(nx, ctd, 1, edgeW, localVec)
                
                # For each (dE, wSum) in localVec, look for (k-1 - dE) in globalDist
                for (dE, wSum) in localVec:
                    need = (k - 1) - dE
                    if need < 0:
                        continue
                    if need in globalDist:
                        cnt, sumW = globalDist[need]
                        # For each of those cnt nodes, total cost = wSum + (that node's cost)
                        # Summation = cnt*wSum + sumW
                        total_undirected_cost += cnt * wSum + sumW
                
                # Now merge localVec into globalDist (small-to-large)
                localMap = defaultdict(lambda: [0, 0])
                for (dE, wSum) in localVec:
                    localMap[dE][0] += 1
                    localMap[dE][1] += wSum
                
                # small-to-large swap if needed
                if len(localMap) > len(globalDist):
                    globalDist, localMap = localMap, globalDist
                
                # merge
                for distE, (lc, lw) in localMap.items():
                    globalDist[distE][0] += lc
                    globalDist[distE][1] += lw
        
        # (d) recurse on subtrees formed by removing 'ctd'
        for (nx, wcost) in graph[ctd]:
            if not used[nx]:
                centroid_decompose(nx)
    
    # Start the decomposition from node 0 (arbitrary)
    centroid_decompose(0)
    
    # Multiply the undirected cost by 2 to account for directed paths
    return 2 * total_undirected_cost
