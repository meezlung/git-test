# type: ignore

from itertools import count

from utils import nums_with_abs

import numth as fast
import numth_brute as brute


sols = (
    fast.is_prime,
    brute.is_prime,
)


def main():
    def inputs():
        for abs_n in count():
            yield from nums_with_abs(abs_n)

    for n in inputs():

        # compute answers
        answers = [sol(n) for sol in sols]

        # print(answers)
        answer = answers[0]

        print(f"{n=} {answer=}")

        assert all(ans == answer for ans in answers), f"answers do not match! expected {answer}, got {answers}"


if __name__ == '__main__':
    main()
