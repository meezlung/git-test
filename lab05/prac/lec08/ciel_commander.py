import sys
sys.setrecursionlimit(10**7)

def solve():
    input_data = sys.stdin.read().strip().split()
    n = int(input_data[0])
    edges_data = input_data[1:]

    # Build adjacency
    adj: list[list[int]] = [[] for _ in range(n)]
    idx = 0
    for _ in range(n-1):
        a = int(edges_data[idx]) - 1
        b = int(edges_data[idx+1]) - 1
        idx += 2
        adj[a].append(b)
        adj[b].append(a)

    # We'll store the final rank letter of each node
    rank = [''] * n
    visited = [False]*n
    subtree_size: list[int] = [0]*n

    def get_sizes(u: int, p: int):
        subtree_size[u] = 1
        for v in adj[u]:
            if v != p and not visited[v]:
                get_sizes(v, u)
                subtree_size[u] += subtree_size[v]

    def get_centroid(u: int, p: int, total: int) -> int:
        for v in adj[u]:
            if v != p and not visited[v]:
                if subtree_size[v] > total//2:
                    return get_centroid(v, u, total)
        return u

    def decompose(start: int, letter: str):
        # 1) compute sizes
        get_sizes(start, -1)
        total = subtree_size[start]
        # 2) find centroid
        c = get_centroid(start, -1, total)

        # 3) label the centroid
        rank[c] = letter
        visited[c] = True

        # 4) Recurse on each connected component
        next_letter = chr(ord(letter)+1)
        if next_letter > 'Z':
            # We exceeded 'Z'; problem states we must print "Impossible!"
            print("Impossible!")
            sys.exit(0)

        for v in adj[c]:
            if not visited[v]:
                decompose(v, next_letter)

    # Call decompose on the whole tree with letter='A'
    decompose(0, 'A')

    # Now 'rank' holds the final labeling. Print in the order of nodes 1..n.
    print(" ".join(rank))

solve()