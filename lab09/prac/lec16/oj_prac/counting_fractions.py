# type: ignore
# How many elements would be contained in the set of reduced proper fractions for d <= 10**6?

def phi_sieve(n):
    """Compute Euler's totient function for all 1..n using a sieve approach."""
    phi = [i for i in range(n+1)]  # phi[k] will end up as phi(k)
    for i in range(2, n+1):
        if phi[i] == i:  # i is prime
            for j in range(i, n+1, i):
                phi[j] -= phi[j] // i
    return phi

d = 10**6
phi_vals = phi_sieve(d)

print(phi_vals)
print(sum(phi_vals) - 1)