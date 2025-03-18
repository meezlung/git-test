# type: ignore

from itertools import product

from utils import CS33Random

from max_matching import max_matching
from max_matching_brute import max_matching as max_matching_brute
from max_matching_flow import max_matching as max_matching_flow


sols = (
    max_matching_brute,
    max_matching_flow,
    max_matching,
)


def main():
    rand = CS33Random(33)

    # ten million tests
    T = 10**7
    for cas in range(T):

        # make random bipartite graph

        while True:
            n = rand.randint(0, rand.choice([3, 5, 7, 8, 9, 10, 11, 12]))
            m = rand.randint(0, rand.choice([3, 5, 7, 8, 9, 10, 11, 12]))
            if min(n, m) <= 7:
                break
        ct = rand.randint(0, min(n*m, rand.choice([n + 5, m + 5, n + m + 5, 2*(n + m + 5), n*m])))
        edges = tuple(rand.sample([*product(range(n), range(m))], ct))

        # compute answers
        answers = [sol(n, m, edges) for sol in sols]

        # print(answers)
        answer = answers[0]

        print(f"Case {cas} of {T}: {n=} {m=} e={len(edges)} {answer=}")

        assert {*answers} == {answer}, f"answers do not match! expected {answer}, got {answers}"


if __name__ == '__main__':
    main()
