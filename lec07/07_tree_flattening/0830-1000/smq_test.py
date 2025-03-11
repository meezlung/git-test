# type: ignore

from utils import CS33Random


from smq_brute import SMQ as SMQBrute
from smq_via_rmq import SMQ as SMQViaRMQ


SMQClasses = (
    SMQBrute,
    SMQViaRMQ,
)


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7

    for cas in range(T):

        n = rand.randint(1, rand.choice([3, 11, 31, 111]))
        q = rand.randint(1, rand.choice([3, 11, 31, 111]))
        V = rand.randint(1, rand.choice([3, 11, 31, 111]))

        def randval():
            return rand.randint(1, V)

        nodes = rand.shuffled(range(n))
        parent = [*range(n)]
        for i in range(1, n):
            parent[nodes[i]] = nodes[rand.randrange(i)]
        root = nodes[0]

        def random_query():
            match rand.getrandbits(1):
                case 0:
                    # update
                    i = rand.randrange(n)
                    v = randval()
                    return 'set', i, v
                case 1:
                    # subtree query
                    i = rand.randrange(n)
                    return 'subtree_min', i
                case _:
                    raise ValueError

        a = [randval() for _ in range(n)]

        queries = [random_query() for _ in range(q)]

        print(f"Trying case {cas} of {T}: {n=} {q=} {V=} {a=} {parent=}")

        # initialize trees
        smqs = [SMQ(a, root, parent) for SMQ in SMQClasses]

        # answer random queries
        for typ, *data in queries:
            match typ:
                case 'set':
                    i, v = data
                    for smq in smqs:
                        smq[i] = v

                case 'subtree_min':
                    i, = data
                    answers = [smq.subtree_min(i) for smq in smqs]

                    assert all(answer == answers[0] for answer in answers)
                case _:
                    raise ValueError


if __name__ == '__main__':
    main()
