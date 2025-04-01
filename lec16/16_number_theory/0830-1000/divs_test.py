# type: ignore

from itertools import count

import numth as fast
import numth_brute as brute


sols = (
    fast.divisors,
    brute.divisors,
)


def main():
    def inputs():
        yield from count(1)

    for n in inputs():

        # compute answers
        answers = [sol(n) for sol in sols]

        # print(answers)
        answer = answers[0]

        print(f"{n=} {answer=}")

        assert all(ans == answer for ans in answers), f"answers do not match! expected {answer}, got {answers}"


if __name__ == '__main__':
    main()
