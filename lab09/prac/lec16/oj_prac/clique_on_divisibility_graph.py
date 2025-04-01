# type: ignore

import sys

n = int(sys.stdin.readline())

A = map(int, sys.stdin.readline().split())

max_val = 10**6 + 1

# mark numbers that are in the set and init dp[x] = 1 for them
present = [False] * max_val

dp = [0] * max_val

for a in A:
    present[a] = True
    dp[a] = 1

best = 1

# dp[j] = max(dp[j], dp[x] + 1)

# process numbers from 1 to max_val - 1
for x in range(1, max_val):
    if not present[x]:
        continue

    curr = dp[x]

    for j in range(x + x, max_val, x): # we iterate x's multiples (j = 2x, 3x, ..., (up to 10**6))
        if present[j]:
            new_val = curr + 1

            if new_val > dp[j]:
                dp[j] = new_val
                
                if new_val > best:
                    best = new_val

print(best)
