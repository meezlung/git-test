import sys
import cmath

PI = 3.141592653589793

def fft(a, invert=False):
    n = len(a)
    if n == 1:
        return a
    # divide
    a_even = fft(a[0::2], invert)
    a_odd  = fft(a[1::2], invert)
    # recombine
    angle = 2 * PI / n * (-1 if invert else 1)
    w = 1+0j
    wn = cmath.exp(angle * 1j)
    y = [0] * n
    for k in range(n // 2):
        u = a_even[k]
        v = a_odd[k] * w
        y[k] = u + v
        y[k + n//2] = u - v
        w *= wn
    return y

def convolution(a, b):
    """
    Given real sequences a and b, returns their linear convolution c,
    where c[s] = sum_{i+j=s} a[i]*b[j], computed via FFT in O(N log N).
    """
    # find power-of-two length
    n = 1
    while n < len(a) + len(b):
        n <<= 1

    # lift into complex and zero-pad
    fa = list(map(complex, a)) + [0] * (n - len(a))
    fb = list(map(complex, b)) + [0] * (n - len(b))

    # FFT → pointwise multiply → inverse FFT
    fa = fft(fa, invert=False)
    fb = fft(fb, invert=False)
    fc = [fa[i] * fb[i] for i in range(n)]
    c_complex = fft(fc, invert=True)

    # round real parts back to integers
    return [int(round(x.real)) for x in c_complex]

if __name__ == '__main__':
    data = sys.stdin.read().split()
    k, n, m = map(int, data[:3])
    apples = list(map(int, data[3:3+n]))
    bananas = list(map(int, data[3+n:3+n+m]))

    # build frequency arrays
    A = [0] * (k + 1)
    B = [0] * (k + 1)
    for w in apples:
        A[w] += 1
    for w in bananas:
        B[w] += 1

    # compute convolution
    C = convolution(A, B)

    # output answers for sums 2..2k
    out = (str(C[s]) if s < len(C) else '0' for s in range(2, 2*k+1))
    sys.stdout.write(' '.join(out))