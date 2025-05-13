
def count_dot_wildcard_matches(pat: str, text: str) -> int:
    """
    Count how many substrings of `text` match the pattern `pat`
    ('.' in pat matches any single character).
    Runs in O(m * |Sigma| + n) time, where m = len(pat) and
    n = len(text).
    """
    m = len(pat)
    n = len(text)
    if m == 0:
        return 0

    # 1) Build the bit‐mask table B:
    #    B[c] has bit j set iff pat[j] == '.' or pat[j] == c.
    B = {}
    # Precompute the "dot‐only" mask: bits where pat[j] == '.'
    dot_mask = 0
    for j, ch in enumerate(pat):
        if ch == '.':
            dot_mask |= (1 << j)

    # Now for every character c that actually occurs in text or pattern,
    # compute B[c].  (Others would behave exactly like an unseen char
    # matching only the dots.)
    alphabet = set(text) | set(ch for ch in pat if ch != '.')
    for c in alphabet:
        mask = dot_mask
        # also set bit j if pat[j] == c
        for j, ch in enumerate(pat):
            if ch == c:
                mask |= (1 << j)
        B[c] = mask

    # 2) Scan the text with one m‐bit register D:
    D = 0
    full = 1 << (m - 1)  # the bit that tells us "we've matched m chars"
    count = 0

    for c in text:
        print(c, D, bin((D << 1) | 1), B.get(c, dot_mask))
        # if c wasn't in alphabet, treat like an "other" char:
        mask = B.get(c, dot_mask)

        # Shift D left by 1, OR in a 1, then AND with mask
        D = ((D << 1) | 1) & mask

        # If the m-th bit is set, we've just matched pat ending here
        if D & full:
            count += 1

    return count


if __name__ == "__main__":
    # Example
    pat  = "a.b"
    text = "xacbb"
    print(f"Pattern: {pat!r}")
    print(f"Text:    {text!r}")
    print("Matches:", count_dot_wildcard_matches(pat, text))
    # Should report matches at positions
    #    text[1:4] = "aca"  (matches a.b with '.'=c)
    #    text[3:6] = "aba"  (matches a.b with '.'=b)
    #    text[7:10] = "bab" (matches a.b with '.'=a)
    # so total = 3
