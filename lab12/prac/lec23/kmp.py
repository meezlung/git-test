
def prefix_function(s: str) -> list:
    n = len(s)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text: str, pattern: str) -> list:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n+1))
    pi = prefix_function(pattern)
    res = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j-1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            res.append(i - m + 1)
            j = pi[j-1]
    return res


def kmp_count(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    # build prefix-function for pattern
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j

    # search
    count = 0
    j = 0
    for ch in text:
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
            if j == m:
                count += 1
                j = pi[j - 1]
    return count