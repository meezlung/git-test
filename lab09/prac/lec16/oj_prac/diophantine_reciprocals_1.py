# type: ignore

import math

def prime_sieve(limit):
    """Return list of primes up to 'limit' using the sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

# Precompute primes up to a certain limit (adjust if needed)
primes = prime_sieve(10**6)

def tau_n2(n):
    """
    Calculate the number of divisors of n^2.
    If n = p1^a1 * p2^a2 * ... then n^2 = p1^(2a1)*p2^(2a2)*...
    and tau(n^2) = (2a1+1)*(2a2+1)*...
    """
    temp = n
    divisor_count = 1
    for p in primes:
        if p * p > temp:
            break
        exponent = 0
        while temp % p == 0:
            exponent += 1
            temp //= p
        if exponent > 0:
            divisor_count *= (2 * exponent + 1)
    if temp > 1:
        # temp is prime
        divisor_count *= (2 * 1 + 1)
    return divisor_count

# We need (tau(n^2) + 1) // 2 > 1000, i.e., tau(n^2) >= 2000
target = 2000
n = 1260
while True:
    if tau_n2(n) >= target:
        print("The smallest n is:", n)
        break
    n += 1
