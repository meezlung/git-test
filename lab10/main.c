// filename: poly_mat_lib.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <complex.h>
#include <math.h>

// ---- 1. Naïve polynomial multiply ----
double* poly_mul_naive(const double *a, int na,
                       const double *b, int nb, int *nr) {
    *nr = na + nb - 1;
    double *r = calloc(*nr, sizeof(double));
    for(int i = 0; i < na; i++)
        for(int j = 0; j < nb; j++)
            r[i+j] += a[i] * b[j];
    return r;
}

// ---- 2. Karatsuba multiply ----
// now takes an 'int *nr' just like poly_mul_naive
double* karatsuba(const double *a, const double *b, int n, int *nr) {
    if (n <= 32) {
        // fallback to naïve
        return poly_mul_naive(a, n, b, n, nr);
    }
    int m = (n + 1) / 2;
    // split a, b
    double *a0 = calloc(m, sizeof(double));
    double *a1 = calloc(n-m, sizeof(double));
    memcpy(a0, a, m*sizeof(double));
    memcpy(a1, a+m, (n-m)*sizeof(double));
    double *b0 = calloc(m, sizeof(double));
    double *b1 = calloc(n-m, sizeof(double));
    memcpy(b0, b, m*sizeof(double));
    memcpy(b1, b+m, (n-m)*sizeof(double));

    int nr0, nr2, nr1;
    double *z0 = karatsuba(a0, b0, m, &nr0);
    double *z2 = karatsuba(a1, b1, n-m, &nr2);

    // compute (a0+a1) and (b0+b1)
    int s_len = m;
    double *sa = calloc(s_len, sizeof(double));
    double *sb = calloc(s_len, sizeof(double));
    for(int i=0;i<s_len;i++){
        sa[i] = a0[i] + (i < n-m ? a1[i] : 0);
        sb[i] = b0[i] + (i < n-m ? b1[i] : 0);
    }
    double *z1 = karatsuba(sa, sb, s_len, &nr1);

    // combine results
    int resn = 2*n - 1;
    double *res = calloc(resn, sizeof(double));
    // add z0
    for(int i=0;i<nr0;i++) res[i] += z0[i];
    // add z2
    for(int i=0;i<nr2;i++) res[i + 2*m] += z2[i];
    // add middle
    for(int i=0;i<nr1;i++){
        double v0 = (i < nr0 ? z0[i] : 0);
        double v2 = (i < nr2 ? z2[i] : 0);
        res[i + m] += z1[i] - v0 - v2;
    }

    *nr = resn;
    // cleanup
    free(a0); free(a1); free(b0); free(b1);
    free(z0); free(z1); free(z2);
    free(sa); free(sb);
    return res;
}

// ---- 3. FFT & convolution ----
void fft(complex double *a, int n) {
    if(n < 2) return;
    int m = n/2;
    complex double *even = calloc(m, sizeof(*even));
    complex double *odd  = calloc(m, sizeof(*odd));
    for(int i=0;i<m;i++){
        even[i] = a[2*i];
        odd[i]  = a[2*i+1];
    }
    fft(even, m);
    fft(odd, m);
    for(int k=0;k<m;k++){
        complex double t = cexp(2.0I*M_PI*k/n) * odd[k];
        a[k]     = even[k] + t;
        a[k+m]   = even[k] - t;
    }
    free(even);
    free(odd);
}

double* poly_mul_fft(const double *a, int na,
                     const double *b, int nb, int *nr) {
    int n = 1;
    while(n < na + nb - 1) n <<= 1;
    complex double *A = calloc(n, sizeof(*A));
    complex double *B = calloc(n, sizeof(*B));
    for(int i=0;i<na;i++) A[i] = a[i];
    for(int i=0;i<nb;i++) B[i] = b[i];
    fft(A,n); fft(B,n);
    for(int i=0;i<n;i++) A[i] *= B[i];
    // inverse FFT
    for(int i=0;i<n;i++) A[i] = conj(A[i]);
    fft(A,n);
    for(int i=0;i<n;i++) A[i] = conj(A[i]) / n;
    *nr = na + nb - 1;
    double *r = calloc(*nr, sizeof(double));
    for(int i=0;i<*nr;i++) r[i] = creal(A[i]);
    free(A); free(B);
    return r;
}

// ---- 4. Naïve matrix multiply ----
double** mat_mul_naive(double **A, double **B, int n) {
    double **C = malloc(n * sizeof(double*));
    for(int i=0;i<n;i++){
        C[i] = calloc(n, sizeof(double));
        for(int k=0;k<n;k++)
            for(int j=0;j<n;j++)
                C[i][j] += A[i][k] * B[k][j];
    }
    return C;
}

// ---- 5. Matrix identity & exponentiation ----
double** mat_identity(int n) {
    double **Id = malloc(n * sizeof(double*));
    for(int i=0;i<n;i++){
        Id[i] = calloc(n, sizeof(double));
        Id[i][i] = 1.0;
    }
    return Id;
}

double** mat_pow(double **A, int n, int k) {
    if(k == 0) return mat_identity(n);
    if(k & 1) {
        double **t = mat_pow(A,n,k-1);
        double **r = mat_mul_naive(A, t, n);
        // you may free t here if you track it
        return r;
    } else {
        double **half = mat_pow(A,n,k/2);
        double **r = mat_mul_naive(half, half, n);
        // free half here if desired
        return r;
    }
}

// ---- Helpers to print ----
void print_poly(const double *p, int n) {
    for(int i=0;i<n;i++){
        printf("%+.2f", p[i]);
        if(i) printf("x^%d ", i);
    }
    printf("\n");
}

void print_mat(double **M, int n) {
    for(int i=0;i<n;i++){
        for(int j=0;j<n;j++){
            printf("%8.2f ", M[i][j]);
        }
        printf("\n");
    }
}

// ---- Sample main() ----
int main(void) {
    // Poly naïve
    double A1[] = {1,2,3}, B1[] = {4,5};
    int nr1;
    double *R1 = poly_mul_naive(A1,3, B1,2, &nr1);
    printf("Naïve poly mul: "); print_poly(R1,nr1); free(R1);

    // Karatsuba (pad to 4)
    double A2[4]={1,2,3,0}, B2[4]={4,5,0,0};
    int nr2;
    double *R2 = karatsuba(A2,B2,4,&nr2);
    printf("Karatsuba:      "); print_poly(R2,nr2); free(R2);

    // FFT
    int nr3;
    double *R3 = poly_mul_fft(A1,3,B1,2,&nr3);
    printf("FFT poly mul:   "); print_poly(R3,nr3); free(R3);

    // Matrices
    int n = 2;
    double **M1 = malloc(n*sizeof(*M1));
    double **M2 = malloc(n*sizeof(*M2));
    double v1[4]={1,2,3,4}, v2[4]={5,6,7,8};
    for(int i=0;i<n;i++){
        M1[i]=malloc(n*sizeof(double));
        M2[i]=malloc(n*sizeof(double));
        for(int j=0;j<n;j++){
            M1[i][j]=v1[i*n+j];
            M2[i][j]=v2[i*n+j];
        }
    }
    printf("\nM1:\n"); print_mat(M1,n);
    printf("M2:\n"); print_mat(M2,n);

    double **M3 = mat_mul_naive(M1,M2,n);
    printf("Naïve M1×M2:\n"); print_mat(M3,n);

    double **M5 = mat_pow(M1,n,5);
    printf("\nM1^5:\n"); print_mat(M5,n);

    // cleanup (omitted for brevity)
    return 0;
}
