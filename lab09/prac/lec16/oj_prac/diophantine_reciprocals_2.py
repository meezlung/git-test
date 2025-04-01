# type: ignore

import math

# We only need the first several primes. For problem 110, the first 15–20 primes is plenty.
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

TARGET = 8_000_000  # We want tau(n^2) >= 8,000,000
best_n = 10**20     # Keep track of the smallest n found so far

def backtrack(i, last_exp, current_n, divisor_count):
    """
    i            = index into 'primes'
    last_exp     = maximum exponent we can assign to primes[i] to keep exponents non-increasing
    current_n    = current value of n built so far
    divisor_count= product of (2*a_j + 1) so far, i.e. partial τ(n^2)
    """
    global best_n

    # If we've already exceeded the required divisor count, update best_n if possible
    if divisor_count >= TARGET:
        if current_n < best_n:
            best_n = current_n
        return

    # If we're out of primes to assign, return
    if i >= len(primes):
        return

    p = primes[i]

    # Try exponents from 'last_exp' down to 0
    # (Ensures exponents are in non-increasing order.)
    for exp in range(last_exp, -1, -1):
        # If multiplying by p^exp would exceed the current best_n, prune (no need to go deeper)
        candidate_n = current_n * (p**exp)
        if candidate_n >= best_n:
            continue

        # Update divisor count if we use exponent 'exp' for prime p
        new_div_count = divisor_count * (2*exp + 1)

        # Recurse or update best_n if it meets the target
        if new_div_count >= TARGET:
            if candidate_n < best_n:
                best_n = candidate_n
        else:
            # Continue to the next prime with exponent bound = exp (non-increasing)
            backtrack(i + 1, exp, candidate_n, new_div_count)

# Start backtracking
backtrack(0, 60, 1, 1)

print("Smallest n with more than 4 million solutions =", best_n)
