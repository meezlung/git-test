MOD = 998244353

# the 8 L-pieces in each 2×2 block spanning columns (i,i+1):
#   first  4 live in rows {0,1}, next 4 in rows {1,2}.
# for each piece s we record:
#   col0[s] = 3-bit mask of its cells in column i
#   col1[s] = 3-bit mask of its cells in column i+1
col0 = [
    0b010,  # remove (0,i) in block {0,1}
    0b001,  # remove (1,i)
    0b011,  # remove (0,i+1)
    0b011,  # remove (1,i+1)
    0b100,  # remove (1,i) in block {1,2}
    0b010,  # remove (2,i)
    0b110,  # remove (1,i+1)
    0b110   # remove (2,i+1)
]
col1 = [
    0b011,  # remove (0,i)
    0b011,  # remove (1,i)
    0b010,  # remove (0,i+1)
    0b001,  # remove (1,i+1)
    0b110,  # remove (1,i)
    0b110,  # remove (2,i)
    0b100,  # remove (1,i+1)
    0b010   # remove (2,i+1)
]

# Build the 8×8 transfer matrix M by brute‐forcing all subsets of the 8 pieces.
M = [[0]*8 for _ in range(8)]
for m_in in range(8):
    # try every subset mask of the 8 pieces
    for subset in range(1<<8):
        m0 = 0  # union of col0‐cells
        m1 = 0  # union of col1‐cells
        ok = True
        for s in range(8):
            if (subset >> s) & 1:
                # piece s must not overlap the incoming mask in col0
                if col0[s] & m_in:
                    ok = False
                    break
                # nor overlap any already chosen piece in col0 or col1
                if (col0[s] & m0) or (col1[s] & m1):
                    ok = False
                    break
                m0 |= col0[s]
                m1 |= col1[s]
        if ok:
            M[m_in][m1] = (M[m_in][m1] + 1) % MOD

# fast 8×8 multiply
def mat_mult(A, B):
    C = [[0]*8 for _ in range(8)]
    for i in range(8):
        for k in range(8):
            a = A[i][k]
            if a:
                for j in range(8):
                    C[i][j] = (C[i][j] + a * B[k][j]) % MOD
    return C

# precompute M^(2^k) for k=0..59
MAXB = 60
Mpows = [None]*MAXB
Mpows[0] = M
for k in range(1, MAXB):
    Mpows[k] = mat_mult(Mpows[k-1], Mpows[k-1])

def ways_to_repair(n: int) -> int:
    # start with column 0 empty:
    vec = [1] + [0]*7
    # multiply vec by M^n via its binary decomposition
    for k in range(MAXB):
        if (n >> k) & 1:
            # vec <- vec * Mpows[k]
            newv = [0]*8
            for j in range(8):
                s = 0
                for i in range(8):
                    s = (s + vec[i] * Mpows[k][i][j]) % MOD
                newv[j] = s
            vec = newv

    # vec[0] = T(n) including the empty placement
    return (vec[0] - 1) % MOD


# Example sanity checks:
if __name__ == "__main__":
    print(ways_to_repair(2))
    print(ways_to_repair(4))

    # for test_n, want in [(2, 10), (4, 194), (3, 38), (5, 848)]:
    #     out = ways_to_repair(test_n)
    #     print(test_n, out, ("OK" if out == want else f"WRONG (got {out})"))
