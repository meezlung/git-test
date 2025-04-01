# type: ignore

import sys

def sieve(n):
    """Return a list of primes up to n (inclusive) using the Sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]

def factorize(x, primes):
    """Return the prime factorization of x as a dict {prime: exponent}."""
    factors = {}
    temp = x
    for p in primes:
        if p * p > temp:
            break
        if temp % p == 0:
            count = 0
            while temp % p == 0:
                count += 1
                temp //= p
            factors[p] = count
    if temp > 1:
        # temp is prime
        factors[temp] = 1
    return factors

N = int(sys.stdin.readline())

A = map(int, sys.stdin.readline().split())

primes = sieve(31622) # sieve up to sqrt(31622)

# for each prime that appears, we want to store the exponent in each number that has it
prime_exponents: dict[int, list[int]] = {}

for number in A:
    factors = factorize(number, primes)
    for p, exp in factors.items():
        if p not in prime_exponents:
            prime_exponents[p] = []
        prime_exponents[p].append(exp)

answer = 1
# For each prime factor encountered, determine the maximum exponent in the gcd
# after one move.
for p, exponents in prime_exponents.items():
    count = len(exponents)
    missing = N - count  # numbers that do NOT contain p (i.e., exponent=0)
    exponents.sort()
    if missing >= 2:
        exp_contrib = 0
    elif missing == 1:
        # one number missing p; we can replace that one.
        # The gcd will have p^(min exponent among numbers that do have it)
        exp_contrib = exponents[0]
    else:  # missing == 0, all numbers already have p
        if len(exponents) >= 2:
            exp_contrib = exponents[1]
        else:
            exp_contrib = exponents[0]
    answer *= p ** exp_contrib
print(answer)