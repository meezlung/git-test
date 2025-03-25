from typing import List, Tuple

def max_matching(n: int, m: int, edges: List[Tuple[int, int]]):

    adj: List[List[int]] = [[] for _ in range(n)]
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

if __name__ == '__main__':
    import sys
    n, m, k = map(int, sys.stdin.readline().split())

    edges: List[Tuple[int, int]] = []
    for _ in range(k):
        i, j = map(int, sys.stdin.readline().split())
        edges.append((i - 1, j - 1))

    ans, to_left = max_matching(n, m, edges)

    print(ans)

    pairs = []
    for idx, left in enumerate(to_left):
        if left != -1:
            print(left + 1, idx + 1)
