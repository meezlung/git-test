#include <stdio.h>

#include "base_conversion.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <complex.h>

#define PI 3.14159265358979323846

// globals for base parameters
static int G_b1, G_b2;

typedef struct {
    char *val;    // converted value in base G_b2
    char *power;  // G_b1^length in base G_b2
} Node;

// strip leading zeros, leave at least one digit
static char *strip(char *s) {
    int i = 0, L = strlen(s);
    while (i + 1 < L && s[i] == '0') {
        i++;
    }
    if (i) {
        memmove(s, s + i, L - i + 1);
    }
    return s;
}

// big-integer addition in base G_b2
static char *add_bigint(const char *A, const char *B) {
    int a = strlen(A), b = strlen(B);
    int L = (a > b ? a : b) + 1;
    char *R = malloc(L + 1);
    R[L] = '\0';
    int carry = 0;
    for (int i = 0; i < L; i++) {
        int da = (a - 1 - i >= 0 ? A[a - 1 - i] - '0' : 0);
        int db = (b - 1 - i >= 0 ? B[b - 1 - i] - '0' : 0);
        int s = da + db + carry;
        R[L - 1 - i] = (s % G_b2) + '0';
        carry = s / G_b2;
    }
    return strip(R);
}

// forward FFT (invert=0) or inverse FFT (invert=1)
static void fft(complex double *a, int n, int invert) {
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) {
            j ^= bit;
        }
        j |= bit;
        if (i < j) {
            complex double tmp = a[i];
            a[i] = a[j];
            a[j] = tmp;
        }
    }
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        complex double wlen = cos(ang) + sin(ang) * I;
        for (int i = 0; i < n; i += len) {
            complex double w = 1;
            for (int j = 0; j < len/2; j++) {
                complex double u = a[i + j];
                complex double v = a[i + j + len/2] * w;
                a[i + j] = u + v;
                a[i + j + len/2] = u - v;
                w *= wlen;
            }
        }
    }
    if (invert) {
        for (int i = 0; i < n; i++) {
            a[i] /= n;
        }
    }
}

// FFT-based multiplication for large sizes
static char *fft_mul(const char *A, const char *B) {
    int a = strlen(A), b = strlen(B);
    int need = 1;
    while (need < a + b) {
        need <<= 1;
    }
    complex double *fa = calloc(need, sizeof *fa);
    complex double *fb = calloc(need, sizeof *fb);
    for (int i = 0; i < a; i++) {
        fa[i] = A[a-1-i] - '0';
    }
    
    for (int i = 0; i < b; i++) {
        fb[i] = B[b-1-i] - '0';
    }
    fft(fa, need, 0);
    fft(fb, need, 0);
    for (int i = 0; i < need; i++) {
        fa[i] *= fb[i];
    }
    fft(fa, need, 1);
    
    char *R = malloc(a + b + 1);
    long long carry = 0;
    int len = a + b;
    for (int i = 0; i < len; i++) {
        long long t = carry + (long long)(creal(fa[i]) + 0.5);
        R[i] = (t % G_b2) + '0';
        carry = t / G_b2;
    }
    while (carry) {
        R[len++] = (carry % G_b2) + '0';
        carry /= G_b2;
    }
    while (len > 1 && R[len-1] == '0') {
        len--;
    }
    for (int i = 0; i < len/2; i++) {
        char tmp = R[i]; R[i] = R[len-1-i]; R[len-1-i] = tmp;
    }
    R[len] = '\0';
    free(fa); free(fb);
    return R;
}

// hybrid multiplication: FFT for large, grade-school for small
static char *mul_bigint(const char *A, const char *B) {
    int a = strlen(A), b = strlen(B);
    if (a > 256 && b > 256) {
        return fft_mul(A, B);
    }
    int L = a + b;
    int *tmp = calloc(L, sizeof(int));
    for (int i = 0; i < a; i++) {
        int da = A[a-1-i] - '0';
        for (int j = 0; j < b; j++) {
            tmp[i+j] += da * (B[b-1-j] - '0');
        }
    }
    for (int i = 0; i < L-1; i++) {
        tmp[i+1] += tmp[i] / G_b2;
        tmp[i] %= G_b2;
    }
    char *R = malloc(L + 1);
    for (int i = 0; i < L; i++) {
        R[L-1-i] = tmp[i] + '0';
    }
    R[L] = '\0';
    free(tmp);
    return strip(R);
}

// recursive divide-and-conquer conversion
static Node convert_rec(const char *s, int n) {
    if (n == 1) {
        Node r;
        int x = s[0] - '0';
        char buf[32]; int t = 0;
        do { buf[t++] = (x % G_b2) + '0'; x /= G_b2; } while (x > 0);
        r.val = malloc(t + 1);
        for (int i = 0; i < t; i++) { r.val[i] = buf[t-1-i]; }
        r.val[t] = '\0';
        int d = G_b1; t = 0;
        do { buf[t++] = (d % G_b2) + '0'; d /= G_b2; } while (d > 0);
        r.power = malloc(t + 1);
        for (int i = 0; i < t; i++) { r.power[i] = buf[t-1-i]; }
        r.power[t] = '\0';
        return r;
    }
    int m = n / 2;
    Node H = convert_rec(s, m);
    Node L = convert_rec(s + m, n - m);
    Node R;
    R.power = mul_bigint(H.power, L.power);
    char *tmp = mul_bigint(H.val, L.power);
    R.val = add_bigint(tmp, L.val);
    free(H.val); free(H.power);
    free(L.val); free(L.power);
    free(tmp);
    return R;
}

char *convert(char *s, int n, int b1, int b2) {
    G_b1 = b1; G_b2 = b2;
    Node R = convert_rec(s, n);
    free(R.power);
    return R.val;
}

// int main() {
//     printf(convert("100001", 6, 2, 10));

//     int n, b1, b2;
//     char *s = malloc(500005);
//     if (scanf("%d %d %d", &n, &b1, &b2) != 3) return 0;
//     scanf("%s", s);
//     char *res = convert(s, n, b1, b2);
//     printf("%s\n", res);
//     free(res);
//     free(s);
//     return 0;
// }
