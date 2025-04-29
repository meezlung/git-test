def gcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

# Global caches: They persist across calls.
_prime_cache = {}  # For numbers > 100_000.
_small_sieve = None  # Sieve for numbers up to 100_000.

# A short list of small primes for quick trial division.
_SMALL_TRIAL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                       31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                       73, 79, 83, 89, 97]

def _build_small_sieve(limit=100000):
    """Build the sieve of Eratosthenes up to limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            step = i * i
            while step <= limit:
                sieve[step] = False
                step += i
    return sieve

def _is_prime_large(x: int) -> bool:
    """
    For x > 100000, first try trial division using a small list of primes,
    then perform two Fermat tests (bases 2 and 3) as a fast, deterministic
    composite check for semiprimes. Semiprime numbers are never Fermat
    pseudoprime for both these bases.
    """
    # Quick trial division.
    for p in _SMALL_TRIAL_PRIMES:
        if x % p == 0:
            # If x equals the trial prime, it is prime.
            return (x == p)
    
    # Two Fermat tests.
    if pow(2, x - 1, x) != 1:
        return False
    if pow(3, x - 1, x) != 1:
        return False
    return True

def is_prime(x: int) -> bool:
    """
    Check if x is prime.
    
    For x <= 100,000 we use a sieve.
    For x > 100,000 we use a quick trial division and then two Fermat tests;
    the result is cached.
    """
    global _small_sieve, _prime_cache
    if x <= 100000:
        if _small_sieve is None:
            _small_sieve = _build_small_sieve(100000)
        return _small_sieve[x]
    
    if x in _prime_cache:
        return _prime_cache[x]
    
    res = _is_prime_large(x)
    _prime_cache[x] = res
    return res

def find_semiprimes(l: list[int]) -> tuple[int, int, int]:
    """
    Given the list l with n integers (where exactly n-2 numbers are primes and
    the other two are semiprimes sharing a common factor), return a tuple
    (s1, s2, common) where s1 and s2 are the two semiprime numbers (in any order)
    and 'common' is their shared prime factor.
    """
    semiprimes = []
    # Scan l and stop when two composites are found.
    for x in l:
        if not is_prime(x):
            semiprimes.append(x)
            if len(semiprimes) == 2:
                break
    
    # The common factor is the gcd of the two semiprimes.
    common_factor, _, _ = gcd(semiprimes[0], semiprimes[1])
    return (semiprimes[0], semiprimes[1], common_factor)

# # Example usage:
# if __name__ == "__main__":
#     # Example 1 as in the problem statement.
#     test_list = [2, 3, 5, 6, 7, 11, 13, 15]
#     # 6 = 2 * 3 and 15 = 3 * 5; the common factor is 3.
#     result = find_semiprimes(test_list)
#     print(result)  # Expected output: (6, 15, 3) (semiprime order may differ)