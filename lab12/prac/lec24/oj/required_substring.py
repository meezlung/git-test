import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def kmp_prefix(pattern):
    m = len(pattern)
    pi = [0]*m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j-1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j
    return pi

def build_automaton(pattern, pi):
    m = len(pattern)
    # nxt[s][c] = next state if at state s and see char c
    nxt = [ [0]*26 for _ in range(m+1) ]
    for s in range(m+1):
        for c in range(26):
            ch = chr(ord('A') + c)
            if s < m and ch == pattern[s]:
                nxt[s][c] = s+1
            else:
                nxt[s][c] = nxt[ pi[s-1] ][c] if s>0 else 0
    return nxt

def main():
    n = int(input())
    P = input().strip()
    m = len(P)
    
    # 1) KMP prefix-function and automaton
    pi = kmp_prefix(P)
    nxt = build_automaton(P, pi)
    
    # 2) DP to count strings of length i ending in state s (<m)
    dp = [0]*(m+1)
    dp[0] = 1
    for _ in range(n):
        ndp = [0]*(m+1)
        for s in range(m):
            if dp[s] == 0: 
                continue
            ways = dp[s]
            for c in range(26):
                s2 = nxt[s][c]
                if s2 < m:
                    ndp[s2] = (ndp[s2] + ways) % MOD
        dp = ndp
    
    avoid = sum(dp[s] for s in range(m)) % MOD
    
    # 3) total strings = 26^n
    total = pow(26, n, MOD)
    answer = (total - avoid) % MOD
    print(answer)

if __name__ == "__main__":
    main()
