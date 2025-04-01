# type: ignore

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def extended_gcd(a, b):
    return _extended_gcd(a, 1, 0, b, 0, 1)


def _extended_gcd(a, xa, ya, b, xb, yb):
    if b == 0:
        return a, xa, ya
    else:
        q = a // b
        return _extended_gcd(b, xb, yb, a - q * b, xa - q * xb, ya - q * yb)


# still relatively slow, but stops at sqrt(n)
def find_prime_factors(n):
    p = 2
    while p <= n:
        if p**2 > n:
            p = n
        while n % p == 0:
            n //= p
            yield p
        p += 1


# still relatively slow; uses find_prime_factors
def is_prime(n):
    return n >= 2 and next(find_prime_factors(n)) == n


def primes(m):
    if m < 2:
        raise ValueError
    is_prime = [True]*(m + 1)
    is_prime[0] = is_prime[1] = False

    pf = [None]*(m + 1)

    for n in range(2, m + 1):
        if is_prime[n]:
            pf[n] = n
            for x in range(2 * n, m + 1, n):
                is_prime[x] = False
                pf[x] = n

    return is_prime, pf


def divisors(m):
    divs = [[] for _ in range(m + 1)]

    for d in range(1, m + 1):
        for n in range(d, m + 1, d):
            divs[n].append(d)

    return divs


