# type: ignore

import math
import math

def sieve(n):
    """Return a list of primes up to n (inclusive) using the Sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i, prime in enumerate(is_prime) if prime]

def count_prime_power_triples(limit=50_000_000):
    # Compute upper bounds for primes in each power term.
    p_bound = int(math.sqrt(limit))
    q_bound = int(limit ** (1/3))
    r_bound = int(limit ** (1/4))
    
    # Generate the prime lists.
    primes_p = sieve(p_bound)
    primes_q = sieve(q_bound)
    primes_r = sieve(r_bound)
    
    results = set()
    
    for p in primes_p:
        p2 = p * p
        if p2 >= limit:
            break  # No need to continue if p^2 itself is too big.
        for q in primes_q:
            q3 = q * q * q
            if p2 + q3 >= limit:
                break  # Further q will only increase the sum.
            for r in primes_r:
                r4 = r ** 4
                total = p2 + q3 + r4
                if total < limit:
                    results.add(total)
                else:
                    break  # Further r will only increase the sum.
                    
    return len(results)

if __name__ == "__main__":
    answer = count_prime_power_triples()
    print(answer)  # Expected output: 1097343
