#include <stdio.h>

// jumping_around.c
#include "jumping_around.h"
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static const uint32_t MOD = 998244353;
static const uint32_t PRIMITIVE_ROOT = 3;

// fast exponentiation modulo MOD
static uint32_t modexp(uint32_t a, uint32_t e) {
    uint64_t res = 1, base = a;
    while (e) {
        if (e & 1) {
            res = (res * base) % MOD;
        }
        base = (base * base) % MOD;
        e >>= 1;
    }
    return res;
}

// in‐place iterative NTT on a[0..n-1], n a power of two.
// if invert = 1, does the inverse transform.
static void ntt(uint32_t *a, size_t n, int invert) {
    // bit‐reverse permutation
    for (size_t i = 1, j = 0; i < n; i++) {
        size_t bit = n >> 1;
        for (; j & bit; bit >>= 1) {
            j ^= bit;
        }
        j |= bit;
        if (i < j) {
            uint32_t t = a[i];
            a[i] = a[j];
            a[j] = t;
        }
    }
    // butterflies
    for (size_t len = 2; len <= n; len <<= 1) {
        uint32_t wlen = modexp(
            PRIMITIVE_ROOT,
            ((MOD - 1) / len) * (invert ? (len - 1) : 1)
        );
        for (size_t i = 0; i < n; i += len) {
            uint64_t w = 1;
            for (size_t j = 0; j < len/2; j++) {
                uint32_t u = a[i+j];
                uint32_t v = (uint32_t)(a[i+j+len/2] * w % MOD);
                uint32_t x = u + v < MOD ? u + v : u + v - MOD;
                uint32_t y = u >= v ? u - v : u + MOD - v;
                a[i+j]         = x;
                a[i+j+len/2]   = y;
                w = (w * wlen) % MOD;
            }
        }
    }
    if (invert) {
        uint32_t inv_n = modexp(n, MOD - 2);
        for (size_t i = 0; i < n; i++) {
            a[i] = (uint32_t)((uint64_t)a[i] * inv_n % MOD);
        }
    }
}

// compute convolution of A[0..nA-1] and B[0..nB-1] modulo MOD.
// returns newly‐malloc’d array of length (nA+nB-1) in *out_n.
static uint32_t* convolution(
    const uint32_t *A, size_t nA,
    const uint32_t *B, size_t nB,
    size_t *out_n
) {
    size_t needed = nA + nB - 1;
    size_t N = 1;
    while (N < needed) {
        N <<= 1;
    }
    uint32_t *fa = calloc(N, sizeof(uint32_t));
    uint32_t *fb = calloc(N, sizeof(uint32_t));
    memcpy(fa, A, nA * sizeof(uint32_t));
    memcpy(fb, B, nB * sizeof(uint32_t));
    ntt(fa, N, 0);
    ntt(fb, N, 0);
    for (size_t i = 0; i < N; i++) {
        fa[i] = (uint32_t)((uint64_t)fa[i] * fb[i] % MOD);
    }
    ntt(fa, N, 1);
    free(fb);
    *out_n = needed;
    return fa;
}

int64_t num_pairs(int n, int64_t *b) {
    // find maximum coordinate
    int64_t maxb = b[0];
    for (int i = 1; i < n; i++) {
        if (b[i] > maxb) {
            maxb = b[i];
        }
    }
    size_t M = (size_t)maxb;

    // build indicator arrays pos[x] = #buildings at x,
    //                       rev[x] = pos[maxb - x]
    uint32_t *pos = calloc(M+1, sizeof(uint32_t));
    uint32_t *rev = calloc(M+1, sizeof(uint32_t));
    for (int i = 0; i < n; i++) {
        pos[b[i]]++;
    }
    for (size_t x = 0; x <= M; x++) {
        rev[M - x] = pos[x];
    }

    // convolve
    size_t conv_n;
    uint32_t *conv = convolution(pos, M+1, rev, M+1, &conv_n);

    // sieve primes up to M
    uint8_t *isprime = malloc(M+1);
    memset(isprime, 1, M+1);
    if (M >= 0) {
        isprime[0] = 0;
    }
    if (M >= 1) {
        isprime[1] = 0;
    }
    for (size_t i = 2; i*i <= M; i++) {
        if (isprime[i]) {
            for (size_t j = i*i; j <= M; j += i) {
                isprime[j] = 0;
            }
        }
    }

    // sum up conv[M - p] for prime p
    int64_t ans = 0;
    for (size_t p = 2; p <= M; p++) {
        if (isprime[p]) {
            size_t idx = M - p;
            // idx < conv_n holds because conv_n = 2*M+1
            ans += conv[idx];
            if (ans >= MOD) {
                ans -= MOD;
            }
        }
    }

    // clean up
    free(pos);
    free(rev);
    free(conv);
    free(isprime);

    return ans;
}

int main() {

    int64_t b[] = {1, 4, 6, 7};
    printf("%ld\n", num_pairs(4, b));

    return 0;
}