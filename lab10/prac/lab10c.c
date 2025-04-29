#include <stdio.h>
#include <assert.h>

// mix_and_match.c
#include "mix_and_match.h"
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

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
    return (uint32_t)res;
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
            uint32_t tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;
        }
    }
    // length‐2,4,8,… butterflies
    for (size_t len = 2; len <= n; len <<= 1) {
        // wlen = primitive_root^{(MOD−1)/len}
        uint32_t wlen = modexp(
            PRIMITIVE_ROOT, (MOD - 1) / len * (invert ? (len - 1) : 1)
        );
        for (size_t i = 0; i < n; i += len) {
            uint64_t w = 1;
            for (size_t j = 0; j < len/2; j++) {
                uint32_t u = a[i+j];
                uint32_t v = a[i+j+len/2] * w % MOD;
                uint32_t x = u + v < MOD ? u + v : u + v - MOD;
                uint32_t y = u >= v ? u - v : u + MOD - v;
                a[i+j]       = x;
                a[i+j+len/2] = y;
                w = (w * wlen) % MOD;
            }
        }
    }
    if (invert) {
        uint32_t inv_n = modexp(n, MOD-2);
        for (size_t i = 0; i < n; i++) {
            a[i] = (uint32_t)((uint64_t)a[i] * inv_n % MOD);
        }
    }
}

// compute convolution of A[0..nA-1] and B[0..nB-1].
// returns newly‐malloc’d array of length nA+nB-1 in *out_n.
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

typedef struct MixAndMatch {
    uint32_t *prefixF;
    size_t lenF;
} MixAndMatch;

MixAndMatch* init(int a, int m, int d,
                 int64_t *A, int64_t *M, int64_t *D) {
    // 1) build histograms
    int64_t maxA = 0, maxM = 0, maxD = 0;
    for(int i=0;i<a;i++) {
        if(A[i]>maxA) {
            maxA=A[i];
        }
    }
    for(int i=0;i<m;i++) {
        if(M[i]>maxM) {
            maxM=M[i];
        }
    }    
    for(int i=0;i<d;i++) {
        if(D[i]>maxD) {
            maxD=D[i];
        }
    }    
    
    size_t sA = maxA+1, sM = maxM+1, sD = maxD+1;
    uint32_t *fA = calloc(sA, sizeof(uint32_t));
    uint32_t *fM = calloc(sM, sizeof(uint32_t));
    uint32_t *fD = calloc(sD, sizeof(uint32_t));
    
    for(int i=0;i<a;i++) {
        fA[A[i]]++;
    }
    for(int i=0;i<m;i++) {
        fM[M[i]]++;
    }
    for(int i=0;i<d;i++) {
        fD[D[i]]++;
    }

    // 2) convolve A*A and M*D
    size_t lenC, lenE;
    uint32_t *C = convolution(fA, sA, fA, sA, &lenC);
    uint32_t *E = convolution(fM, sM, fD, sD, &lenE);

    printf("C ");
    for (int i = 0; i < lenC; i++) {
        printf("%ld ", C[i]);
    }
    printf("\n");

    printf("D ");
    for (int i = 0; i < lenE; i++) {
        printf("%ld ", E[i]);
    }
    printf("\n");

    free(fA); free(fM); free(fD);

    // 3) convolve C*E to get F
    size_t lenF;
    uint32_t *F = convolution(C, lenC, E, lenE, &lenF);

    printf("F ");
    for (int i = 0; i < lenF; i++) {
        printf("%ld ", F[i]);
    }
    printf("\n");

    free(C); free(E);

    // 4) prefix‐sum F in place
    for(size_t i=1;i<lenF;i++) {
        F[i] = (F[i] + F[i-1]) % MOD;
    }

    MixAndMatch *ctx = malloc(sizeof *ctx);
    ctx->prefixF = F;
    ctx->lenF = lenF;
    return ctx;
}

int64_t num_meals(MixAndMatch *mctx, int64_t t) {
    if (t < 0) { return 0; }
    size_t ti = (t >= mctx->lenF ? mctx->lenF - 1 : t);
    return mctx->prefixF[ti];
}

int main() {
    int64_t *A = malloc(4 * sizeof(int64_t));
    int64_t *M = malloc(4 * sizeof(int64_t));
    int64_t *D = malloc(4 * sizeof(int64_t));

    for(int i = 0; i < 4; i++) {
        A[i] = 1;
        M[i] = 1;
        D[i] = 1;
    }

    MixAndMatch *m = init(4, 4, 4, A, M, D);

    assert(num_meals(m, 4) == 256);
    assert(num_meals(m, 3) == 0);

    // TODO add more tests here

    printf("DONE\n");

    return 0;
}
