# type: ignore

from functools import wraps
from itertools import count

import numth as fast
import numth_brute as brute


def with_pf_check(compute_pf):
    @wraps(compute_pf)
    def primes(n):
        is_prime, pf = compute_pf(n)

        # check output of pf
        assert all(pf[k] >= 2 and k % pf[k] == 0 and is_prime[pf[k]] for k in range(2, n + 1))
        
        return is_prime
    return primes


sols = (
    with_pf_check(fast.primes),
    brute.primes,
)


def main():
    def inputs():
        yield from count(2)

    for n in inputs():

        # compute answers
        answers = [sol(n) for sol in sols]

        # print(answers)
        answer = answers[0]

        print(f"{n=} {answer=}")

        assert all(ans == answer for ans in answers), f"answers do not match! expected {answer}, got {answers}"


if __name__ == '__main__':
    main()
