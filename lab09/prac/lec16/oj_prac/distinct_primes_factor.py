# type: ignore
# Find the first four consecutive integers to have four distinct prime factors each. What is the first of these numbers?

from collections import deque
from itertools import count

def find_prime_factors(n: int) -> int:
    """
    Returns a sorted list of the unique prime factors of n using trial division.
    For example: find_prime_factors(360) returns [2, 3, 5]
    """
    n = abs(n)
    factors: set[int] = set()
    # Check for factor 2.
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    # Check odd factors.
    f = 3
    while f * f <= n:
        while n % f == 0:
            factors.add(f)
            n //= f
        f += 2
    if n > 1:
        factors.add(n)
    return len(factors)

def main():
    n = 4

    i = 2

    while True:
        if (find_prime_factors(i) == n and
            find_prime_factors(i + 1) == n and
            find_prime_factors(i + 2) == n and
            find_prime_factors(i + 3) == n):
            print(i, i+1, i+2, i+3)
            return

        i += 1


if __name__ == '__main__':
    main()
