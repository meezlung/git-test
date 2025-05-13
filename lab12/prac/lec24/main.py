'''
Collection of efficient string algorithms useful for programming contests.
Functions included:
  - prefix_function(s)
  - kmp_search(text, pattern)
  - aho_corasick(patterns)
  - suffix_array(s)
  - lcp_array(s, sa)
Usage examples at the bottom.
'''
from collections import deque


def prefix_function(s: str) -> list[int]:
    """
    Computes the prefix function (pi array) for string s.
    pi[i] = length of the longest proper prefix of s[:i+1] which is also a suffix.
    Time: O(n)
    """
    n = len(s)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Finds all occurrences of pattern in text using KMP.
    Returns list of starting indices (0-based) in text where pattern matches.
    Time: O(n + m)
    """
    if not pattern:
        return list(range(len(text) + 1))
    pi = prefix_function(pattern)
    res = []
    j = 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
            if j == len(pattern):
                res.append(i - j + 1)
                j = pi[j - 1]
    return res


class AhoCorasick:
    """
    Aho–Corasick automaton for multi-pattern string matching.
    Build with a list of patterns, then search in text.
    Time: Build O(sum len), Search O(text length + matches).
    """
    def __init__(self, patterns: list[str]):
        self.num_nodes = 1
        self.edges = []           # List of dicts: edges[u][c] = v
        self.fail = []            # failure links
        self.output = []          # output[u] = list of pattern indices ending at u
        for _ in range(1):
            self.edges.append({})
            self.fail.append(0)
            self.output.append([])
        # insert patterns
        for idx, pat in enumerate(patterns):
            u = 0
            for ch in pat:
                if ch not in self.edges[u]:
                    self.edges[u][ch] = self.num_nodes
                    self.edges.append({})
                    self.fail.append(0)
                    self.output.append([])
                    self.num_nodes += 1
                u = self.edges[u][ch]
            self.output[u].append(idx)
        # build failure links
        q = deque()
        for ch, v in self.edges[0].items():
            q.append(v)
            self.fail[v] = 0
        while q:
            u = q.popleft()
            for ch, v in self.edges[u].items():
                q.append(v)
                f = self.fail[u]
                while f > 0 and ch not in self.edges[f]:
                    f = self.fail[f]
                self.fail[v] = self.edges[f].get(ch, 0)
                self.output[v] += self.output[self.fail[v]]

    def search(self, text: str) -> list[tuple[int, int]]:
        """
        Search text for the patterns.
        Returns list of (position, pattern_index) pairs where a pattern ends at position.
        Position is the index in text of the last character of the match.
        """
        u = 0
        results = []
        for i, ch in enumerate(text):
            while u > 0 and ch not in self.edges[u]:
                u = self.fail[u]
            u = self.edges[u].get(ch, 0)
            for pat_idx in self.output[u]:
                results.append((i, pat_idx))
        return results


def suffix_array(s: str) -> list[int]:
    """
    Constructs the suffix array of s. Returns list of starting indices of suffixes in sorted order.
    Time: O(n log n)
    """
    s += chr(0)  # append sentinel
    n = len(s)
    k = 0
    sa = list(range(n))
    rank_arr = [ord(c) for c in s]
    tmp = [0] * n
    def cmp(a, b):
        if rank_arr[a] != rank_arr[b]:
            return rank_arr[a] - rank_arr[b]
        ra = rank_arr[a + k] if a + k < n else -1
        rb = rank_arr[b + k] if b + k < n else -1
        return ra - rb
    while (1 << k) < n:
        sa.sort(key=lambda x: (rank_arr[x], rank_arr[x + k] if x + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i-1]] + (cmp(sa[i-1], sa[i]) < 0)
        rank_arr, tmp = tmp, rank_arr
        k += 1

    return sa[1:]  # drop sentinel index


def inverse_sa(sa: list[int]) -> list[int]:
    """
    Compute inverse of suffix array: inv_sa[i] = position of suffix i in SA.
    """
    n = len(sa)
    inv = [0]*n
    for i, si in enumerate(sa):
        inv[si] = i
    return inv


def lcp_array(s: str, sa: list[int]) -> list[int]:
    """
    Constructs the LCP array using Kasai's algorithm.
    lcp[i] = LCP(sa[i], sa[i+1]).
    Time: O(n)
    """
    n = len(s)
    rank_arr = [0] * n
    for i, idx in enumerate(sa):
        rank_arr[idx] = i
    h = 0
    lcp = [0] * (n - 1)
    for i in range(n):
        if rank_arr[i] == 0:
            continue
        j = sa[rank_arr[i] - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[rank_arr[i] - 1] = h
        if h > 0:
            h -= 1
    return lcp


def lcp_query(i: int, j: int, sa: list[int], lcp: list[int], inv: list[int]) -> int:
    """
    Compute LCP of suffixes at indices i, j using RMQ over lcp array (naive).  
    """
    ri, rj = inv[i], inv[j]
    if ri > rj:
        ri, rj = rj, ri
    return min(lcp[ri:rj]) if ri!=rj else len(sa)-i


def build_nextmatch(p: str, alphabet: set[str]) -> list[dict[str,int]]:
    """
    Build the next-match table for p over given alphabet.
    nextmatch[i][c] = new state after reading c from state i.
    Time: O(m * |alphabet|)
    """
    m = len(p)
    pi = prefix_function(p)
    # allocate table
    nextmatch = [ {c:0 for c in alphabet} for _ in range(m+1) ]
    # state 0
    for c in alphabet:
        nextmatch[0][c] = 1 if m>0 and p[0] == c else 0
    k = 0
    for i in range(1, m+1):
        if i < m:
            for c in alphabet:
                if p[i] == c:
                    nextmatch[i][c] = i + 1
                else:
                    nextmatch[i][c] = nextmatch[pi[i-1]][c]
            k = nextmatch[k][p[i-1]]
    return nextmatch


def fsm_search(t: str, p: str) -> bool:
    """
    Check if p is substring of t via FSM matching.
    """
    if not p:
        return True
    alphabet = set(t) | set(p)
    nextmatch = build_nextmatch(p, alphabet)
    state = 0
    m = len(p)
    for c in t:
        state = nextmatch[state].get(c, 0)
        if state == m:
            return True
    return False

# Example usage
if __name__ == '__main__':
    text = 'ababcababc'
    pat = 'ababc'
    print('KMP matches at:', kmp_search(text, pat))
    patterns = ['he', 'she', 'hers', 'his']
    ac = AhoCorasick(patterns)
    print('AC matches:', ac.search('ahishers'))
    sa = suffix_array('banana')
    print('SA of banana:', sa)
    print('LCP of banana:', lcp_array('banana', sa))


    # Sample text and pattern
    text = "ababcababa"
    pat = "ababa"

    print("Pattern:", pat)
    print("Prefix function:", prefix_function(pat))
    print("KMP search positions:", kmp_search(text, pat))
    print("FSM match found?", fsm_search(text, pat))

    # Suffix array and LCP for a sample string
    sample = "banana"
    sa = suffix_array(sample)
    inv = inverse_sa(sa)
    lcp_arr = lcp_array(sample, sa)

    print("\nString:", sample)
    print("Suffix Array:", sa)
    print("LCP Array:", lcp_arr)
    # LCP of suffixes starting at positions 1 ('anana') and 3 ('ana')
    print("LCP(1,3):", lcp_query(1, 3, sa, lcp_arr, inv))
