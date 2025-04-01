# type: ignore

# slow! all brute force


def is_prime(n):
    return n >= 2 and not any(n % d == 0 for d in range(2, n))


def find_prime_factors(n):
    for p in range(2, n + 1):
        if is_prime(p):
            while n % p == 0:
                n //= p
                yield p


def gcd(a, b):
    return a if b == 0 else b if a == 0 else next(d for d in reversed(range(min(abs(a), abs(b)) + 1)) if a % d == 0 and b % d == 0)


def primes(m):
    return [is_prime(n) for n in range(m + 1)]


def divisors(m):
    return [
        [d for d in range(1, n + 1) if n % d == 0]
        for n in range(m + 1)
    ]
