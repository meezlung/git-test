// string_algorithms.c

#include "string_algorithms.h"
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <complex.h>

// gcc -std=c99 -O2 -lm string_algorithms.c -o myprog

// ---------------------
// ----  TRIE  ---------
// ---------------------

TrieNode* trie_create_node(void) {
    TrieNode *node = calloc(1, sizeof(TrieNode));
    return node;
}

void trie_insert(TrieNode *root, const char *s) {
    TrieNode *v = root;
    v->count++;
    for ( ; *s; s++) {
        int idx = *s - 'a';
        if (!v->next[idx]) v->next[idx] = trie_create_node();
        v = v->next[idx];
        v->count++;
    }
    v->end++;
}

bool trie_search(TrieNode *root, const char *s) {
    TrieNode *v = root;
    for ( ; *s; s++) {
        int idx = *s - 'a';
        if (!v->next[idx]) return false;
        v = v->next[idx];
    }
    return v->end > 0;
}

int trie_count_prefix(TrieNode *root, const char *p) {
    TrieNode *v = root;
    for ( ; *p; p++) {
        int idx = *p - 'a';
        if (!v->next[idx]) return 0;
        v = v->next[idx];
    }
    return v->count;
}

int trie_longest_prefix_match(TrieNode *root, const char *s) {
    TrieNode *v = root;
    int len = 0;
    for ( ; *s; s++) {
        int idx = *s - 'a';
        if (!v->next[idx]) break;
        v = v->next[idx];
        len++;
    }
    return len;
}

int trie_first_mismatch_index(TrieNode *root, const char *s) {
    TrieNode *v = root;
    int i = 0;
    for ( ; *s; s++, i++) {
        int idx = *s - 'a';
        if (!v->next[idx]) return i;
        v = v->next[idx];
    }
    return i;
}

void trie_free(TrieNode *root) {
    if (!root) return;
    for (int i = 0; i < 26; i++)
        trie_free(root->next[i]);
    free(root);
}

// ---------------------
// -- RABIN–KARP  -----
// ---------------------

static const uint64_t RK_B = 257;
static const uint64_t RK_MOD = (uint64_t)1e9 + 7;

static uint64_t compute_hash(const char *s, int m) {
    uint64_t h = 0;
    for (int i = 0; i < m; i++) {
        h = (h * RK_B + (unsigned char)s[i]) % RK_MOD;
    }
    return h;
}

bool is_substring_rk(const char *pat, const char *txt) {
    int m = strlen(pat), n = strlen(txt);
    if (m == 0) return true;
    if (m > n) return false;

    uint64_t pat_h = compute_hash(pat, m);
    uint64_t win_h = compute_hash(txt, m);
    uint64_t pow_b = 1;
    for (int i = 1; i < m; i++) pow_b = (pow_b * RK_B) % RK_MOD;

    if (win_h == pat_h && strncmp(txt, pat, m) == 0) return true;
    for (int i = m; i < n; i++) {
        win_h = (win_h + RK_MOD
                 - (uint64_t)(unsigned char)txt[i-m] * pow_b % RK_MOD) % RK_MOD;
        win_h = (win_h * RK_B + (unsigned char)txt[i]) % RK_MOD;
        if (win_h == pat_h && strncmp(txt + i-m+1, pat, m) == 0)
            return true;
    }
    return false;
}

int count_rk_unoptimized(const char *pat, const char *txt) {
    int m = strlen(pat), n = strlen(txt), cnt = 0;
    if (m == 0) return n + 1;
    if (m > n) return 0;
    uint64_t pat_h = compute_hash(pat, m);
    for (int i = 0; i <= n-m; i++) {
        if (compute_hash(txt+i, m) == pat_h &&
            strncmp(txt+i, pat, m)==0) cnt++;
    }
    return cnt;
}

int count_rk_optimized(const char *pat, const char *txt) {
    int m = strlen(pat), n = strlen(txt), cnt = 0;
    if (m == 0) return n + 1;
    if (m > n) return 0;

    uint64_t pat_h = compute_hash(pat, m),
             win_h = compute_hash(txt, m),
             pow_b = 1;
    for (int i = 1; i < m; i++) pow_b = (pow_b * RK_B) % RK_MOD;

    if (win_h == pat_h && strncmp(txt, pat, m)==0) cnt++;
    for (int i = m; i < n; i++) {
        win_h = (win_h + RK_MOD
                 - (uint64_t)(unsigned char)txt[i-m] * pow_b % RK_MOD) % RK_MOD;
        win_h = (win_h * RK_B + (unsigned char)txt[i]) % RK_MOD;
        if (win_h == pat_h && strncmp(txt+i-m+1, pat, m)==0) cnt++;
    }
    return cnt;
}

int find_first_rk(const char *pat, const char *txt) {
    int m = strlen(pat), n = strlen(txt);
    if (m == 0) return 0;
    if (m > n) return -1;

    uint64_t pat_h = compute_hash(pat, m),
             win_h = compute_hash(txt, m),
             pow_b = 1;
    for (int i = 1; i < m; i++) pow_b = (pow_b * RK_B) % RK_MOD;

    if (win_h == pat_h && strncmp(txt, pat, m)==0) return 0;
    for (int i = m; i < n; i++) {
        win_h = (win_h + RK_MOD
                 - (uint64_t)(unsigned char)txt[i-m] * pow_b % RK_MOD) % RK_MOD;
        win_h = (win_h * RK_B + (unsigned char)txt[i]) % RK_MOD;
        if (win_h == pat_h && strncmp(txt+i-m+1, pat, m)==0)
            return i-m+1;
    }
    return -1;
}

int find_last_rk(const char *pat, const char *txt) {
    int m = strlen(pat), n = strlen(txt), last = -1;
    if (m == 0) return n;
    if (m > n) return -1;

    uint64_t pat_h = compute_hash(pat, m),
             win_h = compute_hash(txt, m),
             pow_b = 1;
    for (int i = 1; i < m; i++) pow_b = (pow_b * RK_B) % RK_MOD;

    if (win_h == pat_h && strncmp(txt, pat, m)==0) last = 0;
    for (int i = m; i < n; i++) {
        win_h = (win_h + RK_MOD
                 - (uint64_t)(unsigned char)txt[i-m] * pow_b % RK_MOD) % RK_MOD;
        win_h = (win_h * RK_B + (unsigned char)txt[i]) % RK_MOD;
        if (win_h == pat_h && strncmp(txt+i-m+1, pat, m)==0)
            last = i-m+1;
    }
    return last;
}

// ---------------------
// ------ KMP ---------
// ---------------------

int* prefix_function(const char *s, int n) {
    int *pi = malloc(n * sizeof(int));
    pi[0] = 0;
    for (int i = 1, j = 0; i < n; i++) {
        while (j > 0 && s[i] != s[j]) j = pi[j-1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

// Returns a malloc'd array of match positions, and sets *out_count
// Caller must free both the returned array and the pi[] inside.
int* kmp_search(const char *pat, const char *txt, int *out_count) {
    int m = strlen(pat), n = strlen(txt);
    int *pi = prefix_function(pat, m);
    int *res = malloc((n+1) * sizeof(int));
    int cnt = 0, j = 0;
    for (int i = 0; i < n; i++) {
        while (j > 0 && txt[i] != pat[j]) j = pi[j-1];
        if (txt[i] == pat[j]) j++;
        if (j == m) {
            res[cnt++] = i - m + 1;
            j = pi[j-1];
        }
    }
    free(pi);
    *out_count = cnt;
    return res;
}

// ---------------------
// --- FFT & MATCH ----
// ---------------------

// Cooley–Tuk FFT, in-place on complex array a of length N (power of two).
static void fft(complex double *a, int N, bool inv) {
    // bit-reverse
    for (int i = 1, j = 0; i < N; i++) {
        int bit = N >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j |= bit;
        if (i < j) {
            complex double tmp = a[i]; a[i] = a[j]; a[j] = tmp;
        }
    }
    // layers
    for (int len = 2; len <= N; len <<= 1) {
        double ang = 2 * acos(-1.0) / len * (inv ? -1 : 1);
        complex double wlen = cexp(I * ang);
        for (int i = 0; i < N; i += len) {
            complex double w = 1;
            for (int j = 0; j < len/2; j++) {
                complex double u = a[i+j];
                complex double v = a[i+j+len/2] * w;
                a[i+j]         = u + v;
                a[i+j+len/2]   = u - v;
                w *= wlen;
            }
        }
    }
    if (inv) {
        for (int i = 0; i < N; i++)
            a[i] /= N;
    }
}

double* convolution(const double *a, const double *b, int n, int m, int *out_len) {
    int N = 1;
    while (N < n + m - 1) N <<= 1;
    complex double *A = calloc(N, sizeof(complex double));
    complex double *B = calloc(N, sizeof(complex double));

    for (int i = 0; i < n; i++) A[i] = a[i];
    for (int i = 0; i < m; i++) B[i] = b[m-1-i];  // reverse b
    fft(A, N, false);
    fft(B, N, false);
    for (int i = 0; i < N; i++) A[i] *= B[i];
    fft(A, N, true);

    int L = n + m - 1;
    double *res = malloc(L * sizeof(double));
    for (int i = 0; i < L; i++) res[i] = creal(A[i]);
    free(A); free(B);
    *out_len = L;
    return res;
}

int* fft_substring_match(const char *pat, const char *txt, int *out_count) {
    int m = strlen(pat), n = strlen(txt);
    if (m > n) { *out_count = 0; return NULL; }

    // map to doubles
    double *A = malloc(n * sizeof(double));
    double *B = malloc(m * sizeof(double));
    for (int i = 0; i < n; i++) A[i] = (double)(unsigned char)txt[i];
    for (int i = 0; i < m; i++) B[i] = (double)(unsigned char)pat[i];

    int conv_len;
    double *C = convolution(A, B, n, m, &conv_len);
    free(A); free(B);

    // prefix sums of A^2
    double *pref = malloc((n+1)*sizeof(double));
    pref[0]=0;
    for (int i=0;i<n;i++) pref[i+1] = pref[i] + (txt[i]*(unsigned char)txt[i]);

    double sum_pat2 = 0;
    for (int i = 0; i < m; i++) sum_pat2 += (unsigned char)pat[i] * (unsigned char)pat[i];

    int *res = malloc((n-m+1)*sizeof(int));
    int cnt = 0;
    for (int k = 0; k <= n-m; k++) {
        double cross = C[k + m - 1];
        double seg2 = pref[k+m] - pref[k];
        double S = seg2 + sum_pat2 - 2*cross;
        if (fabs(S) < 1e-6) res[cnt++] = k;
    }

    free(C);
    free(pref);
    *out_count = cnt;
    return res;
}

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "string_algorithms.h"

int main(void) {
    // ─── 1. Test TRIE ──────────────────────────────────────────────
    TrieNode *trie = trie_create_node();
    const char *words[] = {"apple", "app", "apricot", "banana"};
    for (int i = 0; i < 4; i++) {
        trie_insert(trie, words[i]);
    }
    printf("Trie search 'app': %s\n",
           trie_search(trie, "app") ? "FOUND" : "NOT FOUND");
    printf("Prefix count 'ap': %d\n",
           trie_count_prefix(trie, "ap"));
    printf("Longest prefix of 'appliance': %d\n",
           trie_longest_prefix_match(trie, "appliance"));
    printf("First mismatch in 'appliance': %d\n\n",
           trie_first_mismatch_index(trie, "appliance"));

    // ─── 2. Test RABIN–KARP ────────────────────────────────────────
    const char *text = "abracadabra";
    const char *pat  = "abra";
    printf("is_substring_rk: %s\n\n",
           is_substring_rk(pat, text) ? "YES" : "NO");

    printf("find_first_rk: %d\n", find_first_rk(pat, text));
    printf("find_last_rk:  %d\n", find_last_rk(pat, text));
    printf("count_rk:      %d\n\n", count_rk_unoptimized(pat, text));

    // ─── 3. Test KMP ───────────────────────────────────────────────
    int kmp_count;
    int *kmp_matches = kmp_search(pat, text, &kmp_count);
    printf("KMP found %d match(es) at indices:", kmp_count);
    for (int i = 0; i < kmp_count; i++) {
        printf(" %d", kmp_matches[i]);
    }
    printf("\n\n");
    free(kmp_matches);

    // ─── 4. Test FFT‑SUBSTRING MATCH ─────────────────────────────
    int fft_count;
    int *fft_matches = fft_substring_match(pat, text, &fft_count);
    printf("FFT substring matches (%d):", fft_count);
    for (int i = 0; i < fft_count; i++) {
        printf(" %d", fft_matches[i]);
    }
    printf("\n");
    free(fft_matches);

    // ─── Cleanup ──────────────────────────────────────────────────
    trie_free(trie);
    return 0;
}
