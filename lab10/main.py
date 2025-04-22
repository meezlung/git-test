# Polynomial Multiplication
def poly_mul_naive(a: list[float], b: list[float]) -> list[float]:
    """Multiply two polynomials a and b in coefficient form."""
    m, n = len(a), len(b)
    res = [0]*(m+n-1)
    for i in range(m):
        for j in range(n):
            res[i+j] += a[i]*b[j]
    return res

# Karatsuba
def karatsuba(a: list[float], b: list[float]) -> list[float]:
    """Multiply two polynomials using Karatsuba’s divide‑and‑conquer.  
    Assumes len(a) ≈ len(b)."""
    n = max(len(a), len(b))
    if n <= 1:
        return [ (a[0] if a else 0) * (b[0] if b else 0) ]
    m = (n + 1)//2
    # split a, b into low/high halves
    a_low, a_high = a[:m], a[m:]
    b_low, b_high = b[:m], b[m:]
    z0 = karatsuba(a_low, b_low)
    z2 = karatsuba(a_high, b_high)
    # (a_low + a_high) * (b_low + b_high)
    a_sum = [x+y for x,y in zip(a_low + [0]*(len(a_high)-len(a_low)), a_high)]
    b_sum = [x+y for x,y in zip(b_low + [0]*(len(b_high)-len(b_low)), b_high)]
    z1 = karatsuba(a_sum, b_sum)
    # combine
    res = [0]*(2*n-1)
    for i, v in enumerate(z0):      res[i]     += v
    for i, v in enumerate(z1):      res[i+m]   += v - z0[i if i<len(z0) else 0] - z2[i if i<len(z2) else 0]
    for i, v in enumerate(z2):      res[i+2*m] += v
    return res


# fft based
import cmath

def fft(a: list[complex]) -> list[complex]:
    """Cooley‑Tukey recursive FFT. len(a) must be a power of two."""
    n = len(a)
    if n == 1:
        return a
    even = fft(a[0::2])
    odd  = fft(a[1::2])
    factor = [cmath.exp(2j*cmath.pi*k/n) for k in range(n//2)]
    return [even[k] + factor[k]*odd[k] for k in range(n//2)] + \
           [even[k] - factor[k]*odd[k] for k in range(n//2)]

def ifft(A: list[complex]) -> list[complex]:
    """Inverse FFT via conjugation trick."""
    n = len(A)
    a_conj = [x.conjugate() for x in A]
    inv = fft(a_conj)
    return [x.conjugate()/n for x in inv]

def poly_mul_fft(a: list[float], b: list[float]) -> list[float]:
    """Multiply two real‐coefficient polys via FFT convolution."""
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    # pad
    A = fft([complex(x,0) for x in a] + [0]*(n - len(a)))
    B = fft([complex(x,0) for x in b] + [0]*(n - len(b)))
    C = [A[i]*B[i] for i in range(n)]
    c = ifft(C)
    return [round(c[i].real, 10) for i in range(len(a)+len(b)-1)]


# Matrix Algorithms
def mat_mul_naive(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Multiply two square matrices A and B."""
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def strassen(A, B):
    """Recursive Strassen multiply. n must be a power of 2."""
    n = len(A)
    if n <= 1:
        return [[A[0][0]*B[0][0]]]
    # split into quadrants
    mid = n//2
    A11 = [row[:mid] for row in A[:mid]];  A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]];  A22 = [row[mid:] for row in A[mid:]]
    B11 = [row[:mid] for row in B[:mid]];  B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]];  B22 = [row[mid:] for row in B[mid:]]
    # the seven Strassen products
    def add(X, Y): return [[X[i][j]+Y[i][j] for j in range(len(X))] for i in range(len(X))]
    def sub(X, Y): return [[X[i][j]-Y[i][j] for j in range(len(X))] for i in range(len(X))]
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))
    # recombine
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)
    # assemble full matrix
    top = [C11[i] + C12[i] for i in range(mid)]
    bot = [C21[i] + C22[i] for i in range(mid)]
    return top + bot

def mat_pow(A: list[list[float]], k: int) -> list[list[float]]:
    """Compute A**k in Θ(log k) multiplications."""
    n = len(A)
    # identity
    I = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    if k == 0:
        return I
    if k % 2 == 1:
        return mat_mul_naive(A, mat_pow(A, k-1))
    half = mat_pow(A, k//2)
    return mat_mul_naive(half, half)

def fib(n: int) -> int:
    F = [[1,1],[1,0]]
    M = mat_pow(F, n-1)
    return M[0][0]
