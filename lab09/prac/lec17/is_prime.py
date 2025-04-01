# type: ignore

from random import randrange

def is_prime_brute(n):
    return n >= 2 and not any(n % d == 0 for d in range(2, n))


def is_prime(n, c=100):
    if n < 2:
        return False

    for p in 2,:
        if n == p:
            return True
        if n % p == 0:
            return False

    # Miller Rabin
    (k, m) = (0, n - 1)
    while m % 2 == 0:
        k += 1
        m //= 2

    assert n - 1 == 2**k * m  # slow
    assert k > 0
    assert m % 2 != 0

    def mr_test(a):
        x = pow(a, m, n)
        for _ in range(k):
            if x == 1 or x == n - 1:
                return True
            if (x := x * x % n) == 1:
                return False

        return False

    return all(mr_test(randrange(2, n)) for _ in range(c))


def test():
    N = 10**4
    for n in range(-N, N+1):
        print(n, is_prime(n))
        assert is_prime_brute(n) == is_prime(n)

if __name__ == '__main__':
    test()
