

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


if __name__ == '__main__':
    print(max_matching(5, 4, ( # type: ignore
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 1),
    )))