def count_good_substrings(s: str, mask: str, k: int) -> int:
    n = len(s)

    # Precompute which letters are good
    is_good = [ (c == '1') for c in mask ]

    # Rolling‐hash parameters
    M1, M2 = 10**9+7, 10**9+9
    P1, P2 = 91138233, 97266353

    seen = set()

    for i in range(n):
        bad = 0
        h1 = h2 = 0
        for j in range(i, n):
            if not is_good[ord(s[j]) - ord('a')]:
                bad += 1
                if bad > k:
                    break
            # Append s[j] into the rolling hashes
            v = ord(s[j]) - ord('a') + 1
            h1 = (h1 * P1 + v) % M1
            h2 = (h2 * P2 + v) % M2
            # Combine into one 64‐bit key
            key = (h1 << 32) ^ h2
            seen.add(key)

    return len(seen)

if __name__ == "__main__":
    import sys
    data = sys.stdin.read().split()
    s = data[0].strip()
    mask = data[1].strip()
    k = int(data[2])
    print(count_good_substrings(s, mask, k))
