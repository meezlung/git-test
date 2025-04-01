# type: ignore

from functools import wraps
from itertools import count, product
import math

from utils import divides, nums_with_abs

import numth as fast
import numth_brute as brute


def with_extended_check(ext_gcd):
    @wraps(ext_gcd)
    def gcd(a, b):
        g, x, y = ext_gcd(a, b)

        # check output of extended gcd
        assert divides(g, a)
        assert divides(g, b)
        assert a * x + b * y == g
        
        return g
    return gcd


sols = (
    math.gcd,
    fast.gcd,
    brute.gcd,
    with_extended_check(fast.extended_gcd),
)


def main():
    def inputs():
        for s in count():
            for abs_a in range(s + 1):
                abs_b = s - abs_a
                yield from product(*map(nums_with_abs, (abs_a, abs_b)))

    for a, b in inputs():

        # compute answers (absolute values!)
        answers = [abs(sol(a, b)) for sol in sols]

        # print(answers)
        answer = answers[0]

        print(f"{a=} {b=} {answer=}")

        assert all(ans == answer for ans in answers), f"answers do not match! expected {answer}, got {answers}"


if __name__ == '__main__':
    main()
