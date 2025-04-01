# type: ignore

import math

def max_moves(N):
    # Factorize N
    factors = {}
    temp = N
    # Check factor 2
    while temp % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        temp //= 2
    # Check odd factors
    f = 3
    while f * f <= temp:
        while temp % f == 0:
            factors[f] = factors.get(f, 0) + 1
            temp //= f
        f += 2
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1

    total_moves = 0
    # For each prime factor, compute maximum moves possible
    for p, exponent in factors.items():
        k = 0
        while k * (k + 1) // 2 <= exponent:
            k += 1
        total_moves += k - 1  # subtract one because loop exits when k*(k+1)//2 exceeds exponent
    return total_moves

# Read input, process and print result
if __name__ == '__main__':
    N = int(input().strip())
    print(max_moves(N))
