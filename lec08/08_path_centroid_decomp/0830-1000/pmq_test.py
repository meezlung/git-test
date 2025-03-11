# type: ignore

from pmq_brute import PMQ as PMQBrute
from pmq_via_rmq import PMQ as PMQViaRMQ
from utils import CS33Random


PMQClasses = (
    PMQBrute,
    PMQViaRMQ,
)


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7

    for cas in range(T):

        n = rand.randint(1, rand.choice([3, 11, 31, 51]))
        q = rand.randint(1, rand.choice([3, 11, 31, 51]))
        V = rand.randint(1, rand.choice([11, 31, 111, 311]))

        def randval():
            return rand.randint(1, V)

        edges = rand.random_tree(n)

        assert len(edges) == n - 1

        def random_query():
            match rand.getrandbits(1):
                case 0:
                    # update
                    i = rand.randrange(n)
                    v = randval()
                    return 'set', i, v
                case 1:
                    # path query
                    i, j = (rand.randrange(n) for _ in range(2))
                    return 'path_min', i, j
                case _:
                    raise ValueError

        a = [randval() for _ in range(n)]

        queries = [random_query() for _ in range(q)]

        if cas % 100 == 0:
            print(f"Trying case {cas} of {T}: {n=} {q=} {V=}")

        # initialize trees
        pmqs = [PMQ(a, edges) for PMQ in PMQClasses]

        # answer random queries
        for typ, *data in queries:
            match typ:
                case 'set':
                    i, v = data
                    for pmq in pmqs:
                        pmq[i] = v

                case 'path_min':
                    i, j = data
                    answers = [pmq.path_min(i, j) for pmq in pmqs]

                    # verify
                    assert all(answer == answers[0] for answer in answers)

                case _:
                    raise ValueError


if __name__ == '__main__':
    main()
