# type: ignore

from math import gcd

# -----------------------------------------------------------------------------
# 1. Basic GCD utilities
# -----------------------------------------------------------------------------

def naive_gcd(a: int, b: int) -> int:
    """
    Naive GCD algorithm (trial division approach).
    Returns the greatest common divisor of a and b.
    """
    a, b = abs(a), abs(b)
    smallest = min(a, b)
    best = 1
    for x in range(1, smallest + 1):
        if a % x == 0 and b % x == 0:
            best = x
    return best

def binary_gcd(a: int, b: int) -> int:
    """
    Binary GCD algorithm (also known as Stein's Algorithm).
    Returns the greatest common divisor of a and b.
    """
    a, b = abs(a), abs(b)
    if a == 0:
        return b
    if b == 0:
        return a

    # shift = number of common factors of 2
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1

    while (a & 1) == 0:
        a >>= 1

    while b != 0:
        while (b & 1) == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b = b - a

    return a << shift

def extended_gcd(a: int, b: int):
    """
    Extended Euclidean Algorithm.
    Returns (g, x, y) such that a*x + b*y = g = gcd(a, b).
    """
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

# -----------------------------------------------------------------------------
# 2. Sieve of Eratosthenes and modifications
# -----------------------------------------------------------------------------

def sieve_of_eratosthenes(n: int) -> list:
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

def list_of_divisors_up_to(n: int) -> list:
    """
    Returns a list 'divisors' of length n+1 where divisors[i] is a list of all divisors of i.
    Uses a sieve-like approach.
    """
    divisors = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            divisors[j].append(i)
    return divisors

def smallest_prime_factor_sieve(n: int) -> list:
    """
    Returns a list 'spf' (smallest prime factor) for each number from 0..n.
    spf[x] = smallest prime factor of x, for x >= 2.
    If x is prime, spf[x] = x.
    """
    spf = [0] * (n + 1)
    for i in range(2, n + 1):
        spf[i] = i  # assume i is prime to start

    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # i is prime
            for multiple in range(i * i, n + 1, i):
                # if spf[multiple] is not set yet
                if spf[multiple] == multiple:
                    spf[multiple] = i
    return spf

def prime_factorization(x: int, spf: list) -> dict:
    """
    Given an integer x and a precomputed list of smallest prime factors (spf),
    return a dictionary with prime factors and their exponents.
    Example: prime_factorization(12, spf) -> {2: 2, 3: 1}
    """
    factors = {}
    while x > 1:
        prime_factor = spf[x]
        factors[prime_factor] = factors.get(prime_factor, 0) + 1
        x //= prime_factor
    return factors

def find_prime_factors(n: int) -> list:
    """
    Returns a sorted list of the unique prime factors of n using trial division.
    For example: find_prime_factors(360) returns [2, 3, 5]
    """
    n = abs(n)
    factors = set()
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
    return sorted(factors)

def euler_totient(n: int) -> int:
    """
    Computes Euler's totient function for n, which counts the integers up to n that are coprime with n.
    Uses the prime factors of n obtained via trial division.
    """
    if n == 0:
        return 0
    factors = find_prime_factors(n)
    result = n
    for p in factors:
        result = result // p * (p - 1)
    return result

# -----------------------------------------------------------------------------
# 3. Rational numbers
# -----------------------------------------------------------------------------

class Rational:
    """
    A simple rational number class that represents a fraction (p / q).
    Ensures the fraction is in reduced form.
    """
    __slots__ = ('p', 'q')  # just for memory efficiency

    def __init__(self, p: int, q: int = 1):
        if q == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")
        g = gcd(p, q)
        p //= g
        q //= g
        # Handle negative denominator
        if q < 0:
            p = -p
            q = -q
        self.p = p
        self.q = q

    def __add__(self, other):
        if not isinstance(other, Rational):
            other = Rational(other)
        num = self.p * other.q + other.p * self.q
        den = self.q * other.q
        return Rational(num, den)

    def __sub__(self, other):
        if not isinstance(other, Rational):
            other = Rational(other)
        num = self.p * other.q - other.p * self.q
        den = self.q * other.q
        return Rational(num, den)

    def __mul__(self, other):
        if not isinstance(other, Rational):
            other = Rational(other)
        return Rational(self.p * other.p, self.q * other.q)

    def __truediv__(self, other):
        if not isinstance(other, Rational):
            other = Rational(other)
        return Rational(self.p * other.q, self.q * other.p)

    def __repr__(self):
        return f"{self.p}/{self.q}"

# -----------------------------------------------------------------------------
# 4. Modular arithmetic
# -----------------------------------------------------------------------------

def modular_exponentiation(base: int, exponent: int, mod: int) -> int:
    """
    Computes (base^exponent) mod mod efficiently using binary exponentiation.
    """
    if mod == 1:
        return 0
    result = 1
    base = base % mod
    e = exponent
    while e > 0:
        if e & 1:  # if odd exponent
            result = (result * base) % mod
        base = (base * base) % mod
        e >>= 1
    return result

def solve_system_of_congruences(a_list, n_list):
    """
    Solve a system of congruences using the Chinese Remainder Theorem (CRT).
    The system is:
        x ≡ a_list[i] (mod n_list[i]) for i in [0..k-1]
    Returns x (the smallest non-negative solution) and N = product of n_list.
    Raises ValueError if the system is not consistent.
    """
    # We want to find x such that:
    # x ≡ a1 (mod n1)
    # x ≡ a2 (mod n2)
    # ...
    # We'll do it pair by pair using the standard CRT construction.

    if len(a_list) != len(n_list):
        raise ValueError("Lists must be of same length.")

    # Function to merge two congruences x ≡ a (mod n) and x ≡ b (mod m).
    def merge_congruence(a, n, b, m):
        # Solve: x = a (mod n), x = b (mod m)
        # => a + n*k = b (mod m)
        # => n*k ≡ b - a (mod m)
        g, xg, yg = extended_gcd(n, m)
        if (b - a) % g != 0:
            # no solution
            return None, None
        # Let difference = b - a
        difference = b - a
        # k = xg * difference / g
        k = (xg * (difference // g)) % (m // g)
        # solution for x
        x0 = a + k * n
        # solution is unique modulo lcm(n, m) = n*m/g
        new_mod = (n // g) * m
        x0 %= new_mod
        return x0, new_mod

    x, mod_val = a_list[0], n_list[0]
    for i in range(1, len(a_list)):
        x, mod_val = merge_congruence(x, mod_val, a_list[i], n_list[i])
        if x is None:
            raise ValueError("No solution exists for the given system.")
    return x, mod_val

def modinv(a: int, mod: int) -> int:
    """
    Computes the modular inverse of 'a' under modulo 'mod', which is an integer 'x' such that (a * x) ≡ 1 mod mod.
    Uses the Extended Euclidean Algorithm to find the inverse.
    Raises ValueError if 'a' and 'mod' are not coprime (i.e., gcd(a, mod) != 1).
    """
    g, x, y = extended_gcd(a, mod)
    if g != 1:
        raise ValueError(f"The inverse of {a} modulo {mod} does not exist.")
    return x % mod

# -----------------------------------------------------------------------------
# 5. Additional utilities
# -----------------------------------------------------------------------------

def lcm(a: int, b: int) -> int:
    """
    Returns the least common multiple of a and b.
    """
    return abs(a * b) // gcd(a, b) if a and b else 0

def gcd_list(numbers: list) -> int:
    """
    Returns the greatest common divisor of a list of integers.
    """
    if not numbers:
        return 0
    current_gcd = numbers[0]
    for num in numbers[1:]:
        current_gcd = gcd(current_gcd, num)
        if current_gcd == 1:
            break  # GCD cannot be smaller than 1
    return current_gcd

def lcm_list(numbers: list) -> int:
    """
    Returns the least common multiple of a list of integers.
    """
    if not numbers:
        return 0
    current_lcm = numbers[0]
    for num in numbers[1:]:
        current_lcm = lcm(current_lcm, num)
    return current_lcm

def naive_prime_check(n: int) -> bool:
    """
    Naive primality check. Returns True if n is prime, False otherwise.
    Uses trial division up to sqrt(n).
    """
    if n < 2:
        return False
    if n < 4:
        return True  # 2 or 3
    if n % 2 == 0:
        return n == 2
    r = int(n**0.5)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def trial_division_factorization(n: int) -> dict:
    """
    Factorizes n using trial division.
    Returns a dictionary of prime factors with their exponents.
    """
    n = abs(n)
    factors = {}
    # Count the power of 2
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    # Check odd factors
    f = 3
    while f * f <= n:
        while n % f == 0:
            factors[f] = factors.get(f, 0) + 1
            n //= f
        f += 2
    # If remainder is a prime
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

# -----------------------------------------------------------------------------
# Main entry point (for testing)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Example usage / quick tests
    print("Testing gcd functions:")
    print("naive_gcd(48, 18) =", naive_gcd(48, 18))
    print("binary_gcd(48, 18) =", binary_gcd(48, 18))
    print("extended_gcd(48, 18) =", extended_gcd(48, 18))

    print("\nTesting sieve:")
    prime_bool = sieve_of_eratosthenes(30)
    print(prime_bool)
    print("Primes up to 30:", [i for i, is_p in enumerate(prime_bool) if is_p])

    print("\nTesting smallest_prime_factor_sieve and prime_factorization:")
    spf = smallest_prime_factor_sieve(50)
    print(spf)
    print("Factorization of 48:", prime_factorization(48, spf))

    print("\nTesting Rational class:")
    r1 = Rational(1, 2)
    r2 = Rational(3, 4)
    print("r1 =", r1, ", r2 =", r2)
    print("r1 + r2 =", r1 + r2)
    print("r1 - r2 =", r1 - r2)
    print("r1 * r2 =", r1 * r2)
    print("r1 / r2 =", r1 / r2)

    print("\nTesting modular exponentiation:")
    print("2^10 mod 1000 =", modular_exponentiation(2, 10, 1000))

    print("\nTesting solve_system_of_congruences (CRT):")
    a_list = [2, 3, 2]  # x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
    n_list = [3, 5, 7]
    x_solution, N = solve_system_of_congruences(a_list, n_list)
    print(f"x ≡ {x_solution} (mod {N})")

    print("\nTesting lcm:")
    print("lcm(48, 18) =", lcm(48, 18))

    print("\nTesting naive_prime_check:")
    print("Is 29 prime?", naive_prime_check(29))
    print("Is 30 prime?", naive_prime_check(30))

    print("\nTesting trial_division_factorization:")
    print("Factorization of 360:", trial_division_factorization(360))

    print("\nTesting new functions:")
    print("gcd_list([12, 18, 24]) =", gcd_list([12, 18, 24]))
    print("gcd_list([0, 5, 10]) =", gcd_list([0, 5, 10]))
    print("gcd_list([0, 0]) =", gcd_list([0, 0]))
    print("lcm_list([2, 3, 4]) =", lcm_list([2, 3, 4]))
    print("lcm_list([5, 0, 10]) =", lcm_list([5, 0, 10]))
    print("modinv(3, 11) =", modinv(3, 11))
    print("euler_totient(12) =", euler_totient(12))