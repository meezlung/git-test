# type: ignore

from pmq_brute import offline_pmq as offline_pmq_brute
from pmq_via_rmq import offline_pmq as offline_pmq_via_rmq
from pmq_centroid_decomp import offline_pmq as offline_pmq_centroid_decomp
from utils import CS33Random


sols = (
    offline_pmq_brute,
    offline_pmq_via_rmq,
    offline_pmq_centroid_decomp,
)


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7

    for cas in range(T):

        n = rand.randint(1, rand.choice([3, 11, 31, 111, 311]))
        q = rand.randint(1, rand.choice([3, 11, 31, 111, 311]))
        V = rand.randint(1, rand.choice([11, 31, 111, 311]))

        def randval():
            return rand.randint(1, V)

        edges = rand.random_tree(n)

        assert len(edges) == n - 1

        def random_query():
            i, j = (rand.randrange(n) for _ in range(2))
            return i, j

        a = [randval() for _ in range(n)]

        queries = [random_query() for _ in range(q)]

        if cas % 100 == 0:
            print(f"Trying case {cas} of {T}: {n=} {q=} {V=}")

        answers = [sol(a, edges, queries) for sol in sols]

        # verify
        assert all(answer == answers[0] for answer in answers)


if __name__ == '__main__':
    main()
