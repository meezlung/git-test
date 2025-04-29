// #include <stdio.h>
// #include <assert.h>

#include <stdlib.h>
#include "mix_and_match.h"

typedef struct MixAndMatch{
    int a, m, d; 
    int64_t *A, *M, *D;
} MixAndMatch;


MixAndMatch *init(int a, int m, int d, int64_t *A, int64_t *M, int64_t *D) {
    MixAndMatch *mix_and_match = malloc(sizeof(MixAndMatch));
    mix_and_match->a = a;
    mix_and_match->m = m;
    mix_and_match->d = d;
    mix_and_match->A = A;
    mix_and_match->M = M;
    mix_and_match->D = D;
    return mix_and_match;
}

// double* poly_mul_naive(const double *a, int na,
//                        const double *b, int nb, int *nr) {
//     *nr = na + nb - 1;
//     double *r = calloc(*nr, sizeof(double));
//     for(int i = 0; i < na; i++)
//         for(int j = 0; j < nb; j++)
//             r[i+j] += a[i] * b[j];
//     return r;
// }

// void print_poly(const double *p, int n) {
//     for(int i=0;i<n;i++){
//         printf("%+.2f", p[i]);
//         if(i) printf("x^%d ", i);
//     }
//     printf("\n");
// }

int64_t num_meals(MixAndMatch *m, int64_t t) {
    // Poly Mul

    // double A1[] = {1,1,1,1}, M1[] = {1,1,1,1};
    // int nr1;
    // double *R1 = poly_mul_naive(A1,4, M1,4, &nr1);

    // double D1[] = {1,1,1,1};
    // int nr2;
    // double *R2 = poly_mul_naive(R1,nr1, D1,4, &nr2);

    // int nr3;
    // double *R3 = poly_mul_naive(R2,nr2, A1,4, &nr3);

    // int nr4;
    // double *R4 = poly_mul_naive(R3,nr3, A1,4, &nr4);

    // printf("Naïve poly mul: "); print_poly(R4,nr4); 
    
    // free(R1);
    // free(R2);
    // free(R3);

    int64_t ways = 0;

    for (int i1 = 0; i1 < m->a; i1++){
        for (int i2 = 0; i2 < m->a; i2++) {
            for (int j = 0; j < m->m; j++) {
                for (int k = 0; k < m->d; k++) {
                    int64_t A1 = m->A[i1];
                    int64_t A2 = m->A[i2];
                    int64_t M = m->M[j];
                    int64_t D = m->D[k];

                    int64_t total = A1 + A2 + M + D;

                    if (total <= t) {
                        // printf("%ld %ld %ld %ld = %ld\n", A1, A2, M, D, total);
                        ways += 1;
                    }
                }
            }
        }
    }

    return ways % 998244353;
    // return 256;
}


// int main() {
//     int64_t *A = malloc(4 * sizeof(int64_t));
//     int64_t *M = malloc(4 * sizeof(int64_t));
//     int64_t *D = malloc(4 * sizeof(int64_t));

//     for(int i = 0; i < 4; i++) {
//         A[i] = 1;
//         M[i] = 1;
//         D[i] = 1;
//     }

//     MixAndMatch *m = init(4, 4, 4, A, M, D);

//     printf("%ld\n", num_meals(m, 5));

//     assert(num_meals(m, 4) == 256);
//     // assert(num_meals(m, 3) == 0);

//     // TODO add more tests here

//     printf("DONE\n");

//     return 0;
// }
