# type: ignore

from itertools import combinations, permutations, count

# 0, 1, ..., n-1
# 0, 1, ..., m-1
def max_matching(n, m, edges):
    # edge: {0, ..., n-1} -> {0, ..., m-1}

    edges = set(edges)
    assert has_matching(n, m, edges, 0)
    for k in count():
        if not has_matching(n, m, edges, k + 1):
            return k

def has_matching(n, m, edges, k):
    return any(
        all((i, j) in edges for i, j in zip(l, r, strict=True))
        for l in combinations(range(n), k)
        for r in permutations(range(m), k)
    )


if __name__ == '__main__':
    print(max_matching(5, 4, (
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 1),
    )))
