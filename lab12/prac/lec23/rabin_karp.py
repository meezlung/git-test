
def is_substring(p: str, t: str) -> bool:
    b, p = 257, 10**9 + 7
    n, m = len(t), len(p)

    def compute_hash(word: str):
        h = 0
        for char in word:
            h = (h * b + ord(char)) % p
        return h

    pattern_hash = compute_hash(p)
    window_hash = compute_hash(t[:m])
    b_pow_m = pow(b, m - 1, p)

    for i in range(n - m + 1):
        if window_hash == pattern_hash and t[i:i + m] == p:
            return True
        if i + m < n:
            # slide window
            window_hash = (window_hash * b + ord(t[i + m]) - ord(t[i]) * b_pow_m * b) % p
            window_hash %= p

def count_substring_occurrences_unoptimized(text: str, pattern: str,
                                            b: int = 257,
                                            p: int = 2**61-1) -> int:
    """
    Unoptimized Rabin–Karp: computes the hash of each m‐length window from scratch.
    Time: O(n·m) for hash + occasional character checks.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return n + 1
    if m > n:
        return 0

    # Precompute pattern hash
    def compute_hash(s: str) -> int:
        h = 0
        for c in s:
            h = (h * b + ord(c)) % p
        return h

    pat_hash = compute_hash(pattern)
    count = 0

    # For each window, compute its hash from scratch
    for i in range(n - m + 1):
        window = text[i:i+m]
        if compute_hash(window) == pat_hash:
            # verify to avoid false positives
            if window == pattern:
                count += 1
    return count


def count_substring_occurrences_optimized(text: str, pattern: str,
                                          b: int = 257,
                                          p: int = 2**61-1) -> int:
    """
    Optimized Rabin–Karp: rolling‐hash update in O(1) per shift.
    Time: O(n + m) expected.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return n + 1
    if m > n:
        return 0

    # Precompute b^(m-1) for rolling removal
    b_pow_m1 = pow(b, m-1, p)

    # Initial hashes
    h_pat = 0
    h_win = 0
    for i in range(m):
        h_pat = (h_pat * b + ord(pattern[i])) % p
        h_win = (h_win * b + ord(text[i])) % p

    count = 0
    # Check initial window
    if h_win == h_pat and text[:m] == pattern:
        count += 1

    # Slide window
    for i in range(m, n):
        # Remove leading char, add trailing char
        h_win = (h_win - ord(text[i-m]) * b_pow_m1) % p
        h_win = (h_win * b + ord(text[i])) % p
        # Match?
        if h_win == h_pat and text[i-m+1:i+1] == pattern:
            count += 1

    return count

def find_first_rabin_karp(text: str,
                         pattern: str,
                         b: int = 257,
                         mod: int = 10**9 + 7) -> int:
    """
    Return the first index where `pattern` occurs in `text`,
    or -1 if not found (using rolling‐hash Rabin–Karp).
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1

    # compute initial hashes
    pat_hash = 0
    win_hash = 0
    for i in range(m):
        pat_hash = (pat_hash * b + ord(pattern[i])) % mod
        win_hash = (win_hash * b + ord(text[i]))   % mod
    b_pow = pow(b, m-1, mod)

    # check at position 0
    if win_hash == pat_hash and text[:m] == pattern:
        return 0

    # slide window
    for i in range(m, n):
        win_hash = (win_hash - ord(text[i-m]) * b_pow) % mod
        win_hash = (win_hash * b + ord(text[i]))       % mod
        if win_hash == pat_hash and text[i-m+1:i+1] == pattern:
            return i-m+1

    return -1


def find_last_rabin_karp(text: str,
                        pattern: str,
                        b: int = 257,
                        mod: int = 10**9 + 7) -> int:
    """
    Return the last index where `pattern` occurs in `text`,
    or -1 if not found.
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return n
    if m > n:
        return -1

    # compute pattern hash once
    pat_hash = 0
    for ch in pattern:
        pat_hash = (pat_hash * b + ord(ch)) % mod
    b_pow = pow(b, m-1, mod)

    # rolling hash over text
    win_hash = 0
    for i in range(m):
        win_hash = (win_hash * b + ord(text[i])) % mod

    last = -1
    if win_hash == pat_hash and text[:m] == pattern:
        last = 0

    for i in range(m, n):
        win_hash = (win_hash - ord(text[i-m]) * b_pow) % mod
        win_hash = (win_hash * b + ord(text[i]))       % mod
        idx = i-m+1
        if win_hash == pat_hash and text[idx:idx+m] == pattern:
            last = idx

    return last


def count_rabin_karp(text: str,
                    pattern: str,
                    b: int = 257,
                    mod: int = 10**9 + 7) -> int:
    """
    Return the total number of (possibly overlapping) occurrences
    of `pattern` in `text`.
    """
    return count_substring_occurrences_optimized(text, pattern, b, mod)
