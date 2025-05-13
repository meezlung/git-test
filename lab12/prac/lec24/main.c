/*
 * Collection of efficient string algorithms useful for programming contests.
 * Functions included:
 *   - prefix_function(s, n, pi)
 *   - kmp_search(text, n, pattern, m, res, &res_count)
 *   - AhoCorasick automaton
 *   - suffix_array(s, n, sa)
 *   - lcp_array(s, n, sa, lcp)
 *   - lcp_query(i, j, sa, inv, lcp, n)
 *   - fsm_search(text, n, pattern, m)
 * Usage examples in main().
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

/* Prefix function */
void prefix_function(const char *s, int n, int *pi) {
    pi[0] = 0;
    int j = 0;
    for (int i = 1; i < n; i++) {
        while (j > 0 && s[i] != s[j]) j = pi[j-1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
}

/* KMP search: returns dynamic array of positions, sets res_count */
int *kmp_search(const char *text, int n, const char *pat, int m, int *res_count) {
    int *res = malloc((n+1) * sizeof(int));
    *res_count = 0;
    if (m == 0) {
        for (int i = 0; i <= n; i++) res[(*res_count)++] = i;
        return res;
    }
    int *pi = malloc(m * sizeof(int));
    prefix_function(pat, m, pi);
    int j = 0;
    for (int i = 0; i < n; i++) {
        while (j > 0 && text[i] != pat[j]) j = pi[j-1];
        if (text[i] == pat[j]) j++;
        if (j == m) {
            res[(*res_count)++] = i - m + 1;
            j = pi[j-1];
        }
    }
    free(pi);
    return res;
}

/* Aho-Corasick automaton (lowercase a-z) */
#define ALPHA 26

typedef struct ACNode {
    int next[ALPHA];
    int link;
    int *out;
    int out_size;
} ACNode;

typedef struct AhoCorasick {
    ACNode *nodes;
    int size;
} AhoCorasick;

AhoCorasick *ac_new(int max_nodes) {
    AhoCorasick *ac = malloc(sizeof(*ac));
    ac->nodes = calloc(max_nodes, sizeof(ACNode));
    ac->size = 1;
    for (int c = 0; c < ALPHA; c++) ac->nodes[0].next[c] = -1;
    ac->nodes[0].link = 0;
    ac->nodes[0].out = NULL;
    ac->nodes[0].out_size = 0;
    return ac;
}

void ac_insert(AhoCorasick *ac, const char *pat, int idx) {
    int u = 0;
    for (; *pat; pat++) {
        int c = *pat - 'a';
        if (ac->nodes[u].next[c] == -1) {
            int v = ac->size++;
            ac->nodes[u].next[c] = v;
            for (int k = 0; k < ALPHA; k++) ac->nodes[v].next[k] = -1;
            ac->nodes[v].link = 0;
            ac->nodes[v].out = NULL;
            ac->nodes[v].out_size = 0;
        }
        u = ac->nodes[u].next[c];
    }
    ac->nodes[u].out = realloc(ac->nodes[u].out, (ac->nodes[u].out_size+1)*sizeof(int));
    ac->nodes[u].out[ac->nodes[u].out_size++] = idx;
}

void ac_build(AhoCorasick *ac) {
    int *q = malloc(ac->size * sizeof(int));
    int front = 0, back = 0;
    for (int c = 0; c < ALPHA; c++) {
        int v = ac->nodes[0].next[c];
        if (v != -1) {
            ac->nodes[v].link = 0;
            q[back++] = v;
        } else {
            ac->nodes[0].next[c] = 0;
        }
    }
    while (front < back) {
        int u = q[front++];
        for (int c = 0; c < ALPHA; c++) {
            int v = ac->nodes[u].next[c];
            if (v != -1) {
                int f = ac->nodes[u].link;
                ac->nodes[v].link = ac->nodes[f].next[c];
                int link = ac->nodes[v].link;
                if (ac->nodes[link].out_size) {
                    int sz = ac->nodes[link].out_size;
                    ac->nodes[v].out = realloc(ac->nodes[v].out, (ac->nodes[v].out_size+sz)*sizeof(int));
                    memcpy(ac->nodes[v].out + ac->nodes[v].out_size, ac->nodes[link].out, sz*sizeof(int));
                    ac->nodes[v].out_size += sz;
                }
                q[back++] = v;
            } else {
                ac->nodes[u].next[c] = ac->nodes[ac->nodes[u].link].next[c];
            }
        }
    }
    free(q);
}

int *ac_search(AhoCorasick *ac, const char *text, int n, int *out_count) {
    int *out = malloc(n * 2 * sizeof(int));
    *out_count = 0;
    int u = 0;
    for (int i = 0; i < n; i++) {
        int c = text[i] - 'a';
        u = ac->nodes[u].next[c];
        for (int k = 0; k < ac->nodes[u].out_size; k++) {
            out[(*out_count)*2] = i;
            out[(*out_count)*2+1] = ac->nodes[u].out[k];
            (*out_count)++;
        }
    }
    return out;
}

/* Global variables for suffix-array comparator */
static int n_sa;
static int step_k;
static int *rank_sa;

int cmp_sa(const void *a, const void *b) {
    int i = *(const int*)a;
    int j = *(const int*)b;
    if (rank_sa[i] != rank_sa[j]) return rank_sa[i] - rank_sa[j];
    int ri = (i+step_k <= n_sa ? rank_sa[i+step_k] : -1);
    int rj = (j+step_k <= n_sa ? rank_sa[j+step_k] : -1);
    return ri - rj;
}

/* Suffix array (doubling) */
void suffix_array(const char *s, int n, int *sa) {
    n_sa = n;
    int *rk = malloc((n+1)*sizeof(int));
    int *tmp = malloc((n+1)*sizeof(int));
    for (int i = 0; i <= n; i++) {
        sa[i] = i;
        rk[i] = (i < n ? (unsigned char)s[i] : -1);
    }
    for (step_k = 1; step_k <= n; step_k <<= 1) {
        rank_sa = rk;
        qsort(sa, n+1, sizeof(int), cmp_sa);
        tmp[sa[0]] = 0;
        for (int i = 1; i <= n; i++) {
            tmp[sa[i]] = tmp[sa[i-1]] + (cmp_sa(&sa[i-1], &sa[i]) < 0);
        }
        memcpy(rk, tmp, (n+1)*sizeof(int));
    }
    /* Drop the sentinel index at position 0 */
    memmove(sa, sa+1, n * sizeof(int));
    free(rk);
    free(tmp);
}

/* LCP array (Kasai) */
void lcp_array(const char *s, int n, const int *sa, int *lcp) {
    int *rank = malloc(n*sizeof(int));
    for (int i = 0; i < n; i++) rank[sa[i]] = i;
    int h = 0;
    for (int i = 0; i < n; i++) {
        if (rank[i] > 0) {
            int j = sa[rank[i]-1];
            while (i+h < n && j+h < n && s[i+h] == s[j+h]) h++;
            lcp[rank[i]-1] = h;
            if (h) h--;
        }
    }
    free(rank);
}

int lcp_query(int i, int j, const int *sa, const int *inv, const int *lcp, int n) {
    int ri = inv[i], rj = inv[j];
    if (ri > rj) { int t=ri; ri=rj; rj=t; }
    if (ri == rj) return n - i;
    int mn = INT_MAX;
    for (int k = ri; k < rj; k++) if (lcp[k] < mn) mn = lcp[k];
    return mn;
}

/* FSM substring check */
int fsm_search(const char *text, int n, const char *p, int m) {
    if (m == 0) return 1;
    int *pi = malloc(m*sizeof(int));
    prefix_function(p, m, pi);
    int state = 0;
    for (int i = 0; i < n; i++) {
        while (state>0 && text[i] != p[state]) state = pi[state-1];
        if (text[i] == p[state]) state++;
        if (state == m) { free(pi); return 1; }
    }
    free(pi);
    return 0;
}

int main() {
    const char *text = "ababcababc";
    const char *pat  = "ababc";
    int res_count;
    int *res = kmp_search(text, strlen(text), pat, strlen(pat), &res_count);
    printf("KMP matches at:");
    for (int i = 0; i < res_count; i++) printf(" %d", res[i]);
    printf("\n");
    free(res);

    /* Aho-Corasick example */
    const char *patterns[] = {"he","she","hers","his"};
    AhoCorasick *ac = ac_new(1000);
    for (int i = 0; i < 4; i++) ac_insert(ac, patterns[i], i);
    ac_build(ac);
    int out_count;
    int *out = ac_search(ac, "ahishers", strlen("ahishers"), &out_count);
    printf("AC matches (pos, idx):");
    for (int i = 0; i < out_count; i++) printf(" (%d,%d)", out[2*i], out[2*i+1]);
    printf("\n");
    free(out);

    printf("FSM match found? %s\n",
           fsm_search("ababcababa", strlen("ababcababa"), "ababa", strlen("ababa")) ? "Yes" : "No");
    return 0;
}
