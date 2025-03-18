# type: ignore

from flow import FlowNetwork

# 0, 1, ..., n-1
# 0, 1, ..., m-1
def max_matching(n, m, edges):
    # edge: {0, ..., n-1} -> {0, ..., m-1}

    l = lambda i: i
    r = lambda i: i + n
    s = n + m
    t = s + 1
    fl = FlowNetwork(t + 1, s, t)
    for i in range(n):
        fl.add_edge(s, l(i), 1)
    for j in range(m):
        fl.add_edge(r(j), t, 1)
    for i, j in edges:
        fl.add_edge(l(i), r(j), 1)
    # the matching is encoded in the flow (look for saturated edges)
    return fl.max_flow()

if __name__ == '__main__':
    print(max_matching(5, 4, (
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (3, 1),
    )))
