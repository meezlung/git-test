# from itertools import combinations

# # brute-force for small n,k
# SHAPES = {
#   0:[(0,0),(1,0),(1,1)],
#   1:[(0,0),(0,1),(1,1)],
#   2:[(0,1),(1,0),(1,1)],
#   3:[(0,0),(0,1),(1,0)]
# }
# def count_brute(n, k):
#     # generate every valid L-placement in 3×n
#     P = []
#     for c in range(1,n):
#         for sid, cells in SHAPES.items():
#             for vs in (0,1):
#                 shape = [(r+vs, c-1+col) for (r,col) in cells]
#                 if all(0<=r<3 and 0<=cc<n for (r,cc) in shape):
#                     P.append(tuple(sorted(shape)))
#     P = list(set(P))
#     total = 0
#     for m in range(1, k+1):
#         for combo in combinations(range(len(P)), m):
#             occ = set()
#             ok = True
#             for idx in combo:
#                 for cell in P[idx]:
#                     if cell in occ:
#                         ok = False
#                         break
#                     occ.add(cell)
#                 if not ok:
#                     break
#             if ok:
#                 total += 1
#     return total

def ways_to_repair(n: int, k: int) -> int:
    MOD = 998_244_353
    if k == 0:
        return 0

    # 1) build the 8 L-shapes as (s_mask, n_mask) on a 3×2 block
    base = {
        0: [(0,0),(1,0),(1,1)],
        1: [(0,0),(0,1),(1,1)],
        2: [(0,1),(1,0),(1,1)],
        3: [(0,0),(0,1),(1,0)]
    }
    shapes = []
    for cells in base.values():
        for vs in (0,1):
            sm = nm = 0
            for (r,c) in cells:
                rr = r + vs
                if c == 0:
                    sm |= 1 << rr
                else:
                    nm |= 1 << rr
            shapes.append((sm, nm))

    # 2) build M[next_mask][cur_mask] = poly of length k+1
    def build_M():
        M = [[[0]*(k+1) for _ in range(8)] for _ in range(8)]
        for cur in range(8):
            # try every subset of the 8 shapes (2^8=256 subsets)
            for mask in range(1<<8):
                d = mask.bit_count()
                if d > k:
                    continue
                s_union = n_union = 0
                ok = True
                for i in range(8):
                    if (mask>>i)&1:
                        s,n = shapes[i]
                        # no overlap with cur, nor among themselves
                        if (s & cur) or (s & s_union) or (n & n_union):
                            ok = False
                            break
                        s_union |= s
                        n_union |= n
                if not ok:
                    continue
                M[n_union][cur][d] += 1
        return M

    M = build_M()

    # 3) poly-matrix multiply / pow
    def mat_mul(A, B):
        C = [[[0]*(k+1) for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                acc = [0]*(k+1)
                for t in range(8):
                    a = A[i][t]
                    b = B[t][j]
                    for da in range(len(a)):
                        if a[da]:
                            va = a[da]
                            for db in range(k+1-da):
                                if b[db]:
                                    acc[da+db] = (acc[da+db] + va * b[db]) % MOD
                C[i][j] = acc
        return C

    def mat_pow(X, e):
        # identity
        I = [[[0]*(k+1) for _ in range(8)] for _ in range(8)]
        for i in range(8):
            I[i][i][0] = 1
        R = I
        while e:
            if e & 1:
                R = mat_mul(R, X)
            X = mat_mul(X, X)
            e >>= 1
        return R

    # 4) raise M to the n-th power, apply to g^(0) = e₀
    P = mat_pow(M, n)
    # g^(n)[mask] = P[mask][0]  (since g^(0) is 1 at mask=0, 0 elsewhere)
    poly_end = P[0][0]

    # 5) sum coefficients z^1..z^k
    return sum(poly_end[1:]) % MOD


print(ways_to_repair(2, 1))
print(ways_to_repair(4, 1))



# if __name__ == "__main__":
#     # search for the first mismatch
#     for n in range(2, 11):
#         for k in range(1, 5):
#             brute = count_brute(n, k)
#             fast  = ways_to_repair(n, k)
#             if brute != fast:
#                 print("Mismatch at n={}, k={}: brute={} vs fast={}".format(n, k, brute, fast))
#                 raise SystemExit

#     print("All good up to n=10, k=4")