import cmath
from math import ceil, log2, pi

def fft(arr: list, inv: bool = False) -> None:
    N = len(arr)
    # bit-reversal permutation
    j = 0
    for i in range(1, N):
        bit = N >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
    length = 2
    while length <= N:
        ang = 2 * pi / length * (-1 if inv else 1)
        wlen = cmath.exp(1j * ang)
        for i in range(0, N, length):
            w = 1
            half = length // 2
            for k in range(i, i + half):
                u = arr[k]
                v = arr[k + half] * w
                arr[k] = u + v
                arr[k + half] = u - v
                w *= wlen
        length <<= 1
    if inv:
        for i in range(N):
            arr[i] /= N


def convolution(a: list, b: list) -> list:
    n = 1 << ceil(log2(len(a) + len(b) - 1))
    A = list(map(complex, a)) + [0] * (n - len(a))
    B = list(map(complex, b)) + [0] * (n - len(b))
    fft(A, inv=False)
    fft(B, inv=False)
    for i in range(n):
        A[i] *= B[i]
    fft(A, inv=True)
    return [round(A[i].real) for i in range(len(a) + len(b) - 1)]

def fft_substring_match(text: str, pattern: str) -> list:
    n, m = len(text), len(pattern)
    if m > n:
        return []
    a = [ord(c) for c in text]
    b = [ord(c) for c in pattern]
    # precompute sum of squares for text prefixes
    prefix_a2 = [0] * (n + 1)
    for i in range(n):
        prefix_a2[i+1] = prefix_a2[i] + a[i] * a[i]
    sum_b2 = sum(x*x for x in b)
    # cross-correlation via convolution
    cross = convolution(a, b[::-1])
    matches = []
    for k in range(n - m + 1):
        sum_a2 = prefix_a2[k+m] - prefix_a2[k]
        # S = sum((a[k+i] - b[i])^2) = sum_a2 + sum_b2 - 2*cross[k+m-1]
        if sum_a2 + sum_b2 - 2 * cross[k+m-1] == 0:
            matches.append(k)
    return matches