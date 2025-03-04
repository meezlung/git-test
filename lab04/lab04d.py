# type: ignore

from collections.abc import Sequence


# precompute powers of 10 up to n (so we can do 10^length quickly).
# adjust the maximum size as needed.

MOD = 10**9 + 7
p10 = [1]  # p10[0] = 1

def get_p10(k: int):
    while len(p10) <= k:
        p10.append( (p10[-1] * 10) % MOD )
    return p10[k]


def combine_segment(a: tuple[int, int, int], b: tuple[int, int, int]):
    (fvA, bvA, lenA) = a
    (fvB, bvB, lenB) = b
    # forward value of A||B
    fv = (fvA * get_p10(lenB) + fvB) % MOD
    # backward value of A||B
    bv = (bvB * get_p10(lenA) + bvA) % MOD
    return (fv, bv, lenA + lenB)

def invert_segment(seg: tuple[int, int, int]):
    (fv, bv, length) = seg
    return (bv, fv, length)

class SegmentTree:
    def __init__(self, base_array: Sequence[int]):
        self.n = len(base_array)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.fv = [0] * (2 * self.size)
        self.bv = [0] * (2 * self.size)
        self.length = [0] * (2 * self.size)
        self._build(base_array)

    def _build(self, arr: Sequence[int]):
        # initialize leaves
        for i in range(self.n):
            self.fv[self.size + i] = arr[i] % MOD
            self.bv[self.size + i] = arr[i] % MOD
            self.length[self.size + i] = 1
        # build internal nodes
        for i in range(self.size - 1, 0, -1):
            self._pull(i)

    def _pull(self, idx: int):
        l = 2 * idx
        r = 2 * idx + 1
        lenL = self.length[l]
        lenR = self.length[r]
        self.length[idx] = lenL + lenR
        # forward value
        self.fv[idx] = (self.fv[l] * get_p10(lenR) + self.fv[r]) % MOD
        # backward value
        self.bv[idx] = (self.bv[r] * get_p10(lenL) + self.bv[l]) % MOD

    def update(self, pos: int, val: int):
        # update single position
        idx = pos + self.size
        self.fv[idx] = val % MOD
        self.bv[idx] = val % MOD
        self.length[idx] = 1
        idx //= 2
        while idx > 0:
            self._pull(idx)
            idx //= 2

    def query(self, left: int, right: int):
        res_fv = 0
        res_bv = 0
        res_len = 0
        left += self.size
        right += self.size + 1
        # we'll gather nodes from left side and right side separately
        stack_left = []
        stack_right = []
        while left < right:
            if (left & 1):
                stack_left.append(left)
                left += 1
            if (right & 1):
                right -= 1
                stack_right.append(right)
            left >>= 1
            right >>= 1

        # combine from left to right
        for idx in stack_left:
            seg_len = self.length[idx]
            seg_fv = self.fv[idx]
            seg_bv = self.bv[idx]
            # combine in forward order: res_fv * 10^seg_len + seg_fv
            new_fv = (res_fv * get_p10(seg_len) + seg_fv) % MOD
            new_bv = (seg_bv * get_p10(res_len) + res_bv) % MOD
            res_len += seg_len
            res_fv, res_bv = new_fv, new_bv

        # then combine right side in reverse order
        stack_right.reverse()
        for idx in stack_right:
            seg_len = self.length[idx]
            seg_fv = self.fv[idx]
            seg_bv = self.bv[idx]
            new_fv = (res_fv * get_p10(seg_len) + seg_fv) % MOD
            new_bv = (seg_bv * get_p10(res_len) + res_bv) % MOD
            res_len += seg_len
            res_fv, res_bv = new_fv, new_bv

        return (res_fv, res_bv, res_len)


class DigitMap:
    def __init__(self, connections: Sequence[tuple[int, int]], digits: Sequence[int]):

        self.n = len(digits)
        self.adj: list[list[int]] = [[] for _ in range(self.n+1)]
        for (x, y) in connections:
            self.adj[x].append(y)
            self.adj[y].append(x)

        # store the digits in 1-based 
        self.digits = [0]*(self.n+1)
        for i in range(1, self.n+1):
            self.digits[i] = digits[i-1]

        # HLD arrays
        self.parent = [0]*(self.n+1)
        self.depth = [0]*(self.n+1)
        self.size = [0]*(self.n+1)
        self.heavy = [-1]*(self.n+1)
        self.head = [0]*(self.n+1)
        self.pos = [0]*(self.n+1)

        # DFS to find heavy child
        self._dfs(1, 0)

        # decompose
        self.cur_pos = 0
        self._decompose(1, 1)

        # build array for segment tree
        #   base_array[pos[u]] = digit[u]
        base_array = [0]*self.cur_pos
        for u in range(1, self.n+1):
            base_array[self.pos[u]] = self.digits[u]

        # build segment tree
        self.segtree = SegmentTree(base_array)

    def _dfs(self, u: int, p: int):
        self.parent[u] = p
        self.size[u] = 1
        max_subtree = 0
        for w in self.adj[u]:
            if w == p:
                continue
            self.depth[w] = self.depth[u] + 1
            self._dfs(w, u)
            if self.size[w] > max_subtree:
                max_subtree = self.size[w]
                self.heavy[u] = w
            self.size[u] += self.size[w]

    def _decompose(self, u: int, h: int):
        self.head[u] = h
        self.pos[u] = self.cur_pos
        self.cur_pos += 1

        if self.heavy[u] != -1:
            self._decompose(self.heavy[u], h)

        for w in self.adj[u]:
            if w == self.parent[u] or w == self.heavy[u]:
                continue
            self._decompose(w, w)

    def set_digit(self, i: int, val: int):
        self.digits[i] = val
        # update segment tree
        self.segtree.update(self.pos[i], val)

    def num_coins(self, a: int, b: int):
        return self._query_path(a, b)

    def _query_path(self, u: int, v: int) -> int:
        seg_u = []
        seg_v = []
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] >= self.depth[self.head[v]]:
                # query the chain from head[u] to u in forward order:
                seg = self.segtree.query(self.pos[self.head[u]], self.pos[u])
                # but we actually need it in "u->head[u]" order, so invert:
                seg_u.append(invert_segment(seg))
                u = self.parent[self.head[u]]
            else:
                seg = self.segtree.query(self.pos[self.head[v]], self.pos[v])
                seg_v.append(seg)  # this is already "head[v] -> v" in forward order
                v = self.parent[self.head[v]]

        # wow u and v are in the same chain
        if self.depth[u] > self.depth[v]:
            seg = self.segtree.query(self.pos[v], self.pos[u])
            seg_u.append(invert_segment(seg))
        else:
            seg = self.segtree.query(self.pos[u], self.pos[v])
            seg_v.append(seg)

        # combine everything
        # seg_u is from u -> LCA in reversed order, seg_v is from LCA -> v in forward order
        res = None
        for s in seg_u:
            res = s if res is None else combine_segment(res, s)
        seg_v.reverse()
        for s in seg_v:
            res = s if res is None else combine_segment(res, s)

        return res[0] if res else 0  # The forward-value of the final combination