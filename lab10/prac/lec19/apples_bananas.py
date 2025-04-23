"""
Explanation:
We need to count, for each possible total weight w between 2 and 2k, how many ways there are to pick one apple of weight i and one banana of weight j such that i + j = w.

Let A[i] be the number of apples of weight i, and B[j] be the number of bananas of weight j.  Then the count for a sum s is

    C[s] = \sum_{i + j = s} A[i] * B[j],

which is exactly the discrete convolution of the sequences A and B.  A naive double loop over all i, j would be O(k^2), which is too slow when k can be up to 2·10^5.

However, by using the Fast Fourier Transform (FFT) to compute the convolution in O(N log N) time (where N is the next power of two ≥ 2k+1), we can handle the input limits comfortably.

Steps:
1. Read k, n, m and build frequency arrays A and B of length k+1.
2. Choose N as the smallest power of two ≥ (k+1)+(k+1).
3. Zero-pad A and B to length N.
4. Perform FFT on both arrays, multiply pointwise, then inverse FFT.
5. Round the real parts to the nearest integer to get convolution result C.
6. Output C[2] through C[2k].

Below is a complete Python implementation using a recursive FFT.  It runs in O(N log N) time and uses only built-in types.
"""

import sys
from math import cos, sin, pi

def fft(a, invert=False):
    n = len(a)
    if n == 1:
        return a
    a_even = fft(a[0::2], invert)
    a_odd  = fft(a[1::2], invert)
    angle = 2 * pi / n * (-1 if invert else 1)
    w, wn = 1, complex(cos(angle), sin(angle))
    y = [0] * n
    for k in range(n // 2):
        u = a_even[k]
        v = a_odd[k] * w
        y[k] = u + v
        y[k + n//2] = u - v
        w *= wn
    return y

if __name__ == '__main__':
    data = sys.stdin.read().split()
    k, n, m = map(int, data[:3])
    apples = list(map(int, data[3:3+n]))
    bananas = list(map(int, data[3+n:3+n+m]))

    # Build frequency arrays
    A = [0] * (k + 1)
    B = [0] * (k + 1)
    for w in apples:
        A[w] += 1
    for w in bananas:
        B[w] += 1

    # Find power-of-two length
    N = 1
    while N < len(A) + len(B):
        N <<= 1
    # Zero pad
    A += [0] * (N - len(A))
    B += [0] * (N - len(B))

    # FFT convolution
    FA = fft(list(map(complex, A)))
    FB = fft(list(map(complex, B)))
    FC = [FA[i] * FB[i] for i in range(N)]
    C = fft(FC, invert=True)

    # Extract integer results and print sums from 2..2k
    out = []
    for s in range(2, 2*k + 1):
        val = int(round(C[s].real)) if s < len(C) else 0
        out.append(str(val))
    sys.stdout.write(' '.join(out))
