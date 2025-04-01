# type: ignore

def phi_sieve(n):
    """Compute Euler's totient function for all 1..n using a sieve approach."""
    phi = list(range(n+1))  # phi[k] will end up as phi(k)
    for i in range(2, n+1):
        if phi[i] == i:  # i is prime
            for j in range(i, n+1, i):
                phi[j] -= phi[j] // i
    return phi

limit = 10**7
phi_vals = phi_sieve(limit)

best_n = 1
best_ratio = float('inf')

for x in range(2, limit+1):
    # detect permutation here
    if sorted(str(x)) == sorted(str(phi_vals[x])):
        ratio = x / phi_vals[x]
        if ratio < best_ratio:
            best_ratio = ratio
            best_n = x

print(best_n)
print(best_ratio)
