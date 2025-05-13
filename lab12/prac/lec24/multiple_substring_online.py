class RMQ:
    """
    Range Minimum Query using a sparse table for O(1) queries.
    Preprocess: O(n log n), Query: O(1)
    """
    def __init__(self, arr):
        import math
        self.n = len(arr)
        self.LOG = self.n.bit_length()
        self.st = [arr.copy()]
        for k in range(1, self.LOG):
            prev = self.st[k-1]
            curr = []
            length = 1 << k
            half = length >> 1
            for i in range(self.n - length + 1):
                curr.append(min(prev[i], prev[i + half]))
            self.st.append(curr)

    def query(self, l, r):
        """Query minimum on arr[l..r] inclusive"""
        import math
        length = r - l + 1
        k = length.bit_length() - 1
        return min(self.st[k][l], self.st[k][r - (1 << k) + 1])


def build_suffix_array(s):
    """Doubling algorithm: O(n log n)"""
    n = len(s)
    sa = list(range(n))
    rank_ = [ord(c) for c in s] + [-1]
    tmp = [0] * n
    k = 1
    while k < n:
        sa.sort(key=lambda i: (rank_[i], rank_[i + k] if i + k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, curr = sa[i-1], sa[i]
            tmp[curr] = tmp[prev] + ((rank_[prev], rank_[prev+k] if prev+k<n else -1) <
                                      (rank_[curr], rank_[curr+k] if curr+k<n else -1))
        rank_, tmp = tmp, rank_
        k <<= 1
    return sa


def build_lcp(s, sa):
    """Kasai's algorithm: O(n)"""
    n = len(s)
    rank_ = [0]*n
    for i, si in enumerate(sa):
        rank_[si] = i
    lcp = [0]*(n-1)
    h = 0
    for i in range(n):
        if rank_[i] == 0:
            continue
        j = sa[rank_[i]-1]
        while i+h < n and j+h < n and s[i+h] == s[j+h]:
            h += 1
        lcp[rank_[i]-1] = h
        if h:
            h -= 1
    return lcp

class SubstringQuery:
    def __init__(self, t):
        self.t = t
        self.n = len(t)
        self.sa = build_suffix_array(t)
        self.lcp = build_lcp(t, self.sa)
        self.rmq = RMQ(self.lcp)

    def is_substring(self, p):
        """Returns True if p is a substring of t."""
        n, sa, t = self.n, self.sa, self.t
        # find leftmost suffix >= p
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if t[sa[mid]:] < p:
                lo = mid + 1
            else:
                hi = mid
        left = lo
        # find leftmost suffix > p prefix
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if t[sa[mid]:].startswith(p):
                lo = mid + 1
            elif t[sa[mid]:] < p:
                lo = mid + 1
            else:
                hi = mid
        right = lo
        return left < right

# Example usage:
# t = "banana"
# q = SubstringQuery(t)
# print(q.is_substring("ana"))  # True
# print(q.is_substring("nab"))  # False
