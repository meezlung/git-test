# type: ignore

from itertools import count

def nums_with_abs(v):
    # yield -v
    if v > 0:
        yield v

def find_prime_factors(n):
    yield 1
    p = 2
    while p <= n:
        if p**2 > n:
            p = n
        while n % p == 0:
            n //= p
            yield p
        p += 1

def main():
    def inputs():
        for abs_n in range(100):
            yield from nums_with_abs(abs_n)

    for n in inputs():

        # compute answers
        answers = [list(find_prime_factors(n))]

        answer = answers[0]

        print(f"{n=} {answer=}")

if __name__ == "__main__":
    main()
        