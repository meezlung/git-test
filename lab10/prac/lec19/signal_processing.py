import sys
import threading

def fft(a, invert):
    """
    In-place Cooley–Tuk FFT (iterative) on array a of complex numbers.
    If invert=True, computes inverse FFT.
    """
    import math
    n = len(a)
    # bit-reversal permutation
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    # FFT
    length = 2
    while length <= n:
        ang = 2 * math.pi / length * (-1 if invert else 1)
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = 1+0j
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w
                a[j] = u + v
                a[j + length // 2] = u - v
                w *= wlen
        length <<= 1
    # if inverse FFT, divide by n
    if invert:
        for i in range(n):
            a[i] /= n


def convolution(a, b):
    """
    Computes convolution of real sequences a and b via FFT,
    returning a list of real values (rounded to nearest integer).
    """
    import math
    n, m = len(a), len(b)
    size = 1
    while size < n + m - 1:
        size <<= 1
    fa = [complex(x, 0) for x in a] + [0] * (size - n)
    fb = [complex(x, 0) for x in b] + [0] * (size - m)

    fft(fa, False)
    fft(fb, False)
    for i in range(size):
        fa[i] *= fb[i]
    fft(fa, True)

    # round real parts to nearest integer
    result = [int(round(fa[i].real)) for i in range(n + m - 1)]
    return result


def main():
    data = sys.stdin.read().strip().split()
    n, m = map(int, data[:2])
    a = list(map(int, data[2:2+n]))
    b = list(map(int, data[2+n:2+n+m]))

    # reverse mask for correlation-like convolution
    b.reverse()
    res = convolution(a, b)

    print(' '.join(map(str, res)))

if __name__ == '__main__':
    # for faster I/O and to avoid recursion limits
    threading.Thread(target=main).start()
