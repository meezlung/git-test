# type: ignore
# How many elements would be contained in the set of reduced proper fractions for d <= 10**6 between 1/3 and 1/2?

import math

def count_fractions(limit):
    count = 0
    for d in range(2, limit + 1):
        # Calculate the range for numerator n:
        n_min = d // 3 + 1  # smallest n such that n/d > 1/3
        n_max = (d - 1) // 2  # largest n such that n/d < 1/2
        for n in range(n_min, n_max + 1):
            if math.gcd(n, d) == 1:
                count += 1
    return count

if __name__ == "__main__":
    limit = 12_000
    result = count_fractions(limit)
    print(result)
