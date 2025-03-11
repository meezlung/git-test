# type: ignore

from utils import CS33Random


from rmq_brute import RMQ as RMQBrute
from rmq_sqrt import RMQ as RMQSqrt
from rmq_segtree import RMQ as RMQSegTree


RMQClasses = (
    RMQBrute,
    RMQSqrt,
    RMQSegTree,
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

        def random_query():
            match rand.getrandbits(1):
                case 0:
                    # update
                    i = rand.randrange(n)
                    v = randval()
                    return 'set', i, v
                case 1:
                    # range query
                    i, j = sorted(rand.randint(0, n) for _ in range(2))
                    return 'range_min', i, j
                case _:
                    raise ValueError

        a = [randval() for _ in range(n)]

        queries = [random_query() for _ in range(q)]

        print(f"Trying case {cas} of {T}: {n=} {q=} {V=} {a=}")

        # initialize trees
        rmqs = [RMQ(a) for RMQ in RMQClasses]

        # answer random queries
        for typ, *data in queries:
            match typ:
                case 'set':
                    i, v = data
                    for rmq in rmqs:
                        rmq[i] = v

                case 'range_min':
                    i, j = data
                    answers = [rmq.range_min(i, j) for rmq in rmqs]

                    assert all(answer == answers[0] for answer in answers)
                case _:
                    raise ValueError


if __name__ == '__main__':
    main()
