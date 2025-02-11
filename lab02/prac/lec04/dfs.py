

def search(n: int, adj_list: list[list[int]]) -> list[list[int]]:
    vis = [False] * n

    comps: list[list[int]] = []

    def dfs(i: int):
        assert not vis[i]
        vis[i] = True

        comps[-1].append(i)

        for j in adj_list[i]:
            if not vis[j]:
                dfs(j)

    
    for s in range(n):
        if not vis[s]:
            comps.append([])
            dfs(s)

    return comps


if __name__ == '__main__':
    print(search(5, [
        [1, 4],
        [0],
        [3],
        [2],
        [0],
    ]))