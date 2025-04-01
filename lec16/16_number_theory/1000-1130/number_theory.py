# type: ignore

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def extended_gcd(a, b):
    """
    g = gcd(a, b)
    aX + bY = g, find X and Y

    b = 0:
    g, X, Y = a, 1, 0
    a * 1 + b * 0 = a

    b > 0:
    g, x, y = gcd(b, a % b)
    bx + (y * (a % b)) = g
    bx + (a - (a // b * b))y = g
    bx + ay - (a // b * b)y = g
    ay + b(x - (a // b * y))

    X = y
    Y = x - (y * (a // b))
    """
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (y * (a // b))


def diophantine(a, b, c):
    """
    ax + by = c, d = gcd(a, b)

    c must be divisible by d
    """
    g, x, y = extended_gcd(a, b)
    if c % g == 0:
        k = c // g
        return x * k, y * k
    else:
        return None, None


def sieve_of_eratosthenes(n):
    """
    returns all primes in [2, n]
    """
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    # largest prime factor
    lpf = [i for i in range(n + 1)]
    for i in range(2, n + 1):
        if sieve[i]:
            for j in range(2 * i, n + 1, i):
                sieve[j] = False
                lpf[j] = i
    return sieve, lpf


def prime_factors(n):
    l = []
    _, lpf = sieve_of_eratosthenes(n)

    while n > 1:
        l.append(lpf[n])
        n //= lpf[n]
    return l


def divisor_sieve(n):
    """
    returns divisors of numbers in [2, n]
    """
    divs = [[] for _ in range(n + 1)]
    for d in range(1, n + 1):
        for k in range(d, n + 1, d):
            divs[k].append(d)
    return divs


def totient(n):
    """
    len(m for m in range(1, n) if gcd(m, n) == 1)
    """
    divs_n = divisor_sieve(n)
    # print(divs_n[n])
    return n - len(divs_n[n]) + 1


def mod_inv(a, n):
    # gcd(a, n) = 1
    # find a' such that aa' % n = 1
    g, x, y = extended_gcd(a, n)
    assert a * x + n * y == 1
    return x


def crt(a, m, b, n):
    assert gcd(m, n) == 1
    r = (b - a) * mod_inv(m, n) % n
    return a + r * m, m * n


assert diophantine(12, 8, 68) == (17, -17)

assert totient(22) == 19

# print(prime_factors(2 * 3 * 5 * 7 * 9 * 11 * 13))

# print(mod_inv(12, 7))

# print(crt(9, 12, 6, 7))

