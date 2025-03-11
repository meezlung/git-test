from collections.abc import Sequence

PancakeTower = Sequence[int]

class PancakeTowers:
    def __init__(self, p0: PancakeTower, p1: PancakeTower, p2: PancakeTower):
        self.base = [list(p0), list(p1), list(p2)]

        self.prefix: list[list[int]] = []
        for arr in self.base:
            pf = [0]
            for r in arr:
                pf.append(pf[-1] + r)
            self.prefix.append(pf)

        # caches
        self.len_versions: dict[int, int] = {
            0: len(p0),
            1: len(p1),
            2: len(p2),
        }

        self.sum_memo: dict[tuple[int, int, int], int] = {}

        super().__init__()


    def get_length(self, k: int) ->  int:
        if k in self.len_versions:
            return self.len_versions[k]
        
        # L(k) = ceil(2/3 * L(k-3)) + ceil(2/3 * L(k-2))
        L_km3 = self.get_length(k - 3)
        L_km2 = self.get_length(k - 2)
        T = (2*L_km3 + 2) // 3  
        B = (2*L_km2 + 2) // 3  
        length_k = T + B
        self.len_versions[k] = length_k
        return length_k

    def sum_base(self, base_idx: int, i: int, j: int) -> int:
        arr_len = len(self.base[base_idx])
        if i < 1: i = 1
        if j > arr_len: j = arr_len
        if i > j:
            return 0
        pf = self.prefix[base_idx]
        return pf[j] - pf[i-1]
    
    def sum_radii(self, k: int, i: int, j: int) -> int:
        # iterative
        # 1) clamp i..j
        Lk = self.get_length(k)
        if i < 1: i = 1
        if j > Lk: j = Lk
        if i > j:
            return 0

        # If we already memo'd, return
        main_key = (k, i, j)
        if main_key in self.sum_memo:
            return self.sum_memo[main_key]

        sub_ans: dict[tuple[int,int,int], int] = {}

        # We'll push the main query
        stack: list[tuple[int, int, int, int, int]] = []
        stack.append((k, i, j, 0, 0))  

        while stack:
            (cur_k, cur_i, cur_j, _, _) = stack.pop()

            # If already in global sum_memo, no need to re-compute
            if (cur_k, cur_i, cur_j) in self.sum_memo:
                continue

            # If in sub_ans from a prior step, we are done too
            if (cur_k, cur_i, cur_j) in sub_ans:
                # That means we computed it, but not yet written to self.sum_memo
                self.sum_memo[(cur_k, cur_i, cur_j)] = sub_ans[(cur_k, cur_i, cur_j)]
                continue

            # clamp again (should be redundant)
            length_ck = self.get_length(cur_k)
            if cur_i < 1: cur_i = 1
            if cur_j > length_ck: cur_j = length_ck
            if cur_i > cur_j:
                # sum=0
                self.sum_memo[(cur_k, cur_i, cur_j)] = 0
                continue

            # base case?
            if cur_k < 3:
                # direct from base prefix sums
                base_idx = cur_k
                ans = self.sum_base(base_idx, cur_i, cur_j)
                sub_ans[(cur_k, cur_i, cur_j)] = ans
                self.sum_memo[(cur_k, cur_i, cur_j)] = ans
                continue

            # otherwise, we do the top/bottom decomposition:
            L_km3 = self.get_length(cur_k - 3)
            L_km2 = self.get_length(cur_k - 2)
            T_len = (2*L_km3 + 2)//3
            B_len = (2*L_km2 + 2)//3

            top_start, top_end = 1, T_len
            bot_start, bot_end = T_len+1, T_len + B_len

            # we'll gather up to two subcalls:
            top_subcall_needed = False
            bot_subcall_needed = False
            top_subkey = None
            bot_subkey = None
            local_sum = 0

            # check overlap with top portion
            if cur_j >= top_start and cur_i <= top_end:
                si = max(cur_i, top_start)
                sj = min(cur_j, top_end)
                top_subkey = (cur_k-3, si, sj)
                if top_subkey in self.sum_memo:
                    local_sum += self.sum_memo[top_subkey]
                else:
                    top_subcall_needed = True

            # check overlap with bottom portion
            if cur_j >= bot_start and cur_i <= bot_end:
                si = max(cur_i, bot_start)
                sj = min(cur_j, bot_end)
                offset = (L_km2 - B_len)  # so bot_start => offset+1
                si_prime = offset + (si - bot_start + 1)
                sj_prime = offset + (sj - bot_start + 1)
                bot_subkey = (cur_k-2, si_prime, sj_prime)
                if bot_subkey in self.sum_memo:
                    local_sum += self.sum_memo[bot_subkey]
                else:
                    bot_subcall_needed = True

            if not (top_subcall_needed or bot_subcall_needed):
                # We have everything we need, store final answer
                sub_ans[(cur_k, cur_i, cur_j)] = local_sum
                self.sum_memo[(cur_k, cur_i, cur_j)] = local_sum
                # done with this frame
            else:
                # We still need subcalls. We'll push the current frame back
                # with state=1, partial=local_sum so we can add subcalls later.
                stack.append((cur_k, cur_i, cur_j, 1, local_sum))

                # Then push subcalls that are not computed:
                if top_subcall_needed and top_subkey is not None:
                    (sk, si, sj) = top_subkey
                    if (sk, si, sj) not in self.sum_memo:
                        stack.append((sk, si, sj, 0, 0))

                if bot_subcall_needed and bot_subkey is not None:
                    (sk, si, sj) = bot_subkey
                    if (sk, si, sj) not in self.sum_memo:
                        stack.append((sk, si, sj, 0, 0))

        # after the while‑loop, sum_memo[main_key] is guaranteed to be computed
        return self.sum_memo[main_key]
