# Find the sum of all the primes below two million.

def sieve_of_eratosthenes(n: int) -> list[bool]:
    """
    Returns a list of booleans, where is_prime[i] = True if i is prime, else False.
    The sieve is computed up to n (inclusive).
    """
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    return is_prime


def main():
    n = 2_000_000
    primes = sieve_of_eratosthenes(n)

    sum = 0
    for i, num in enumerate(primes):
        if num:
            sum += i

    print(sum)


if __name__ == '__main__':
    main()