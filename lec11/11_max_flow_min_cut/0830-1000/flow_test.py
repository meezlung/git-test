# type: ignore

from utils import Edge, CS33Random
from flow import FlowNetwork


flow_net_classes = (
    FlowNetwork,
)


def verify_max_flow_min_cut(FlowNetwork, n, s, t, edges):
    # minor checks that the input is valid
    assert 0 <= s < n
    assert 0 <= t < n
    assert s != t
    assert all(isinstance(edge, Edge) for edge in edges)

    # construct flow network
    flow = FlowNetwork(n, s, t)
    for edge in edges:
        assert edge.cost >= 0
        flow.add_edge(edge.i, edge.j, edge.cost)

    # compute flow
    max_flow_value = flow.max_flow()

    # verify flow conservation constraints
    for i in range(n):
        if i not in {s, t}:
            assert flow.netflow(i) == 0

    # verify flow value
    assert flow.netflow(s) == -flow.netflow(t) == max_flow_value >= 0

    # construct cut (S, T)
    vis = [False]*n
    vis[s] = True
    stak = [s]
    while stak:
        i = stak.pop()
        assert vis[i]
        for edge in flow.adj[i]:
            if not edge.is_saturated and not vis[edge.j]:
                vis[edge.j] = True
                stak.append(edge.j)

    # verify that the cut (S, T) is valid
    assert vis[s] and not vis[t]

    # verify max flow = min cut
    min_cut_cost = sum(edge.cost for edge in edges if vis[edge.i] and not vis[edge.j])
    assert max_flow_value == min_cut_cost

    # check that edges from S to T are saturated
    # this check includes reverse/back edges
    for i in range(n):
        for edge in flow.adj[i]:
            if vis[edge.i] and not vis[edge.j]:
                assert edge.is_saturated

    return max_flow_value


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7
    for cas in range(T):

        # make random flow network
        n = rand.randint(2, rand.choice([3, 11, 21, 31, 41]))
        e = rand.randint(0, rand.choice([3, 11, 31, 111, n, 2*n, n**2//2, n**2, 2*n**2]))
        V = rand.randint(1, rand.choice([3, 11, 31, 111]))
        s, t = rand.sample(range(n), 2)
        def rand_edge():
            i = rand.randrange(n)
            j = rand.randrange(n)
            cap = rand.randint(0, V)
            return Edge(i, j, cap)
        edges = [rand_edge() for _ in range(e)]

        # compute answers
        answers = [verify_max_flow_min_cut(FlowNetwork, n, s, t, edges) for FlowNetwork in flow_net_classes]
        # print(answers)
        answer = answers[0]

        print(f"Case {cas} of {T}: {n=} {e=} {V=} {answer=}")

        assert {*answers} == {answer}, f"answers do not match! expected {answer}, got {answers}"


if __name__ == '__main__':
    main()
