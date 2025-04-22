import math


def dft(a):
    """
    Compute the discrete Fourier transform (DFT) of list a (complex), O(n^2).
    Returns a new list of length n.
    """
    n = len(a)
    A = [0+0j] * n
    for k in range(n):
        sum_k = 0+0j
        for j in range(n):
            angle = 2 * math.pi * j * k / n
            sum_k += a[j] * complex(math.cos(angle), math.sin(angle))
        A[k] = sum_k
    return A


def idft(A):
    """
    Compute the inverse DFT of list A (complex), O(n^2).
    Returns a new list of length n.
    """
    n = len(A)
    a = [0+0j] * n
    for j in range(n):
        sum_j = 0+0j
        for k in range(n):
            angle = 2 * math.pi * j * k / n
            sum_j += A[k] * complex(math.cos(angle), -math.sin(angle))
        a[j] = sum_j / n
    return a


def _bit_reverse_permute(a):
    """
    In-place bit-reversal reorder for list a (length power of two).
    """
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]


def fft(a, invert=False):
    """
    In-place Cooley–Tukey FFT on list a of complex numbers, O(n log n).

    Parameters:
        a (list of complex): input sequence, length must be power of two.
        invert (bool): False for forward FFT, True for inverse FFT.
    """
    n = len(a)
    _bit_reverse_permute(a)

    length = 2
    while length <= n:
        angle = 2 * math.pi / length * (-1 if invert else 1)
        wlen = complex(math.cos(angle), math.sin(angle))

        for i in range(0, n, length):
            w = 1 + 0j
            half = length // 2
            for j in range(half):
                u = a[i + j]
                v = a[i + j + half] * w
                a[i + j] = u + v
                a[i + j + half] = u - v
                w *= wlen
        length <<= 1

    if invert:
        for i in range(n):
            a[i] /= n


if __name__ == "__main__":
    # DFT and IDFT of a simple sequence
    x = [1, 2, 3, 4]
    X = dft([complex(val) for val in x])
    print("DFT of", x, "->", X)
    print("Inverse DFT recovers", idft(X))

    # FFT and IFFT of a simple sequence (in-place)
    y = [complex(val) for val in x]
    fft(y, invert=False)
    print(f"FFT of {x}:", y)
    fft(y, invert=True)
    print("Inverse FFT recovers:", y)


    # Polynomial multiplication via DFT and IDFT
    # (1 + 2x + 3x^2) * (4 + 5x)
    p = [1, 2, 3]
    q = [4, 5]
    m = len(p) + len(q) - 1
    # pad to next power of two
    n = 1
    while n < m:
        n <<= 1
    # DFT-based convolution
    P = dft([complex(val) for val in p] + [0] * (n - len(p)))
    Q = dft([complex(val) for val in q] + [0] * (n - len(q)))
    R = [P[i] * Q[i] for i in range(n)]
    r = idft(R)
    prod_dft = [round(r[i].real) for i in range(m)]
    print("Polynomial product via DFT:", prod_dft)


    # Polynomial multiplication via FFT and IFFT (faster for large n)
    a = [complex(val) for val in p] + [0] * (n - len(p))
    b = [complex(val) for val in q] + [0] * (n - len(q))
    fft(a, invert=False)
    fft(b, invert=False)
    for i in range(n):
        a[i] *= b[i]
    fft(a, invert=True)
    prod_fft = [round(a[i].real) for i in range(m)]
    print("Polynomial product via FFT:", prod_fft)
