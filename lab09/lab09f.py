def overall_excitement(power_levels):
    # Preliminaries
    n = len(power_levels)
    if n < 2:
        return 0
    M = max(power_levels)
    
    # Frequency array for each power level 1..M
    freq = [0]*(M+1)
    for p in power_levels:
        freq[p] += 1

    # Compute Mobius function mu[1..M]
    mu = [1]*(M+1)
    is_prime = [True]*(M+1)
    primes = []
    for i in range(2, M+1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i*p > M:
                break
            is_prime[i*p] = False
            if i % p == 0:
                mu[i*p] = 0
                break
            else:
                mu[i*p] = -mu[i]
                
    # Precompute for every d: 
    #   cnt[d] = number of x in power_levels that are divisible by d,
    #   T[d] = sum over x (where d|x) of (x//d)^2,
    #   U[d] = sum over x (where d|x) of (x//d)^4.
    cnt = [0]*(M+1)
    T = [0]*(M+1)
    U = [0]*(M+1)
    for d in range(1, M+1):
        for j in range(d, M+1, d):
            if freq[j]:
                cnt[d] += freq[j]
                a = j // d
                T[d] += freq[j] * (a*a)
                U[d] += freq[j] * (a**4)
                
    # Compute sums S_gcd and S_lcm using Mobius inversion.
    S_gcd = 0
    S_lcm = 0
    # Loop over d from 1 to M; inner loop over multiples m
    for d in range(1, M+1):
        # d^2 factor
        d2 = d*d
        inner_gcd = 0
        inner_lcm = 0
        m = 1
        while d*m <= M:
            u = d*m
            # For gcd: add μ(m)*C(cnt[u],2)
            if cnt[u] >= 2:
                inner_gcd += mu[m] * (cnt[u]*(cnt[u]-1)//2)
            # For lcm: if at least 2 elements, (T[u]^2 - U[u]) is nonzero.
            if cnt[u] >= 2:
                # Using m^4 factor.
                inner_lcm += mu[m] * (m**4) * ((T[u]*T[u] - U[u])//2)
            m += 1
        S_gcd += d2 * inner_gcd
        S_lcm += d2 * inner_lcm

    # Compute sum_{i<j} x_i*y_j = ((sum x)^2 - sum(x^2))//2.
    tot = sum(power_levels)
    tot2 = sum(x*x for x in power_levels)
    prod_sum = (tot*tot - tot2) // 2

    overall = S_lcm + S_gcd - 2*prod_sum
    return overall

# # For testing:
# if __name__ == '__main__':
#     # Example 1:
#     print(overall_excitement((2, 3, 4)))  # Expected output: 150
#     print(overall_excitement((1, 1, 1)))  # Expected output: 0
