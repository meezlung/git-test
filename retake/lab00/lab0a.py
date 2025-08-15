from collections import deque

def fastest_resilience(n_0: int) -> int:
    if n_0 <= 0:
        return 0
    
    dp = [0] * (n_0 + 1) # base case na rin na dp[0] = 0
    
    for n in range(1, n_0 + 1):
        min_num_of_moves = float('inf')
        s = n
        seen = 0 # bitmask for digits 1->9
        while s:
            d = s % 10
            s //= 10
            if d == 0: # useless
                continue 

            if (seen >> d) & 1: # this is so that we don't process the same digit twice
                continue

            seen |= 1 << d

            sq = d*d
            if sq >= n:
                min_num_of_moves = 1 # dp[n] = 1 if digit d of n is d^2 >= n
                break # oks na

            cand = 1 + dp[n - sq] # dp[n] = 1 + min(dp[n - d^2]) <- d is an elem of digits(n), d>0
            if cand < min_num_of_moves:
                min_num_of_moves = cand

        dp[n] = min_num_of_moves

    return dp[n]

print(fastest_resilience(13))
print(fastest_resilience(98))
print(fastest_resilience(214))
print(fastest_resilience(32))
print(fastest_resilience(200000))