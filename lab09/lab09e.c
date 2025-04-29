#include <stdlib.h>
#include <stdint.h>
#include "puzzle_pairing.h"
typedef struct { int x, y; } P;
typedef struct { int L, R, y, id, sg; } Q;
static inline void bit_upd(int *B, int n, int i, int v) { for(; i<=n; i+= i & -i) { B[i]+= v; } }
static inline int bit_qry(int *B, int i) { int s=0; for(; i; i-= i & -i) { s+= B[i]; } return s; }
static int64_t *calcF(int n) {
    int64_t *f = (int64_t*)calloc(n+1, sizeof(int64_t));
    if(!f) { { exit(1); } }
    for(int i=1; i<= n/2; i++) { { for(int j=2*i; j<= n; j+= i) { { f[j]+= i; } } } }
    { return f; }
}
static void countSortP(P *arr, int n, int range) {
    int *cnt = (int*)calloc(range+1, sizeof(int));
    if(!cnt) { { exit(1); } }
    for(int i=0; i<n; i++) { { cnt[arr[i].y]++; } }
    for(int i=1; i<= range; i++) { { cnt[i]+= cnt[i-1]; } }
    P *out = (P*)malloc(n * sizeof(P));
    if(!out) { { exit(1); } }
    for(int i=n-1; i>=0; i--) { { out[--cnt[arr[i].y]] = arr[i]; } }
    for(int i=0; i<n; i++) { { arr[i] = out[i]; } }
    free(out); free(cnt);
}
static void countSortQ(Q *arr, int n, int range) {
    int *cnt = (int*)calloc(range+1, sizeof(int));
    if(!cnt) { { exit(1); } }
    for(int i=0; i<n; i++) { { cnt[arr[i].y]++; } }
    for(int i=1; i<= range; i++) { { cnt[i]+= cnt[i-1]; } }
    Q *out = (Q*)malloc(n * sizeof(Q));
    if(!out) { { exit(1); } }
    for(int i=n-1; i>=0; i--) { { out[--cnt[arr[i].y]] = arr[i]; } }
    for(int i=0; i<n; i++) { { arr[i] = out[i]; } }
    free(out); free(cnt);
}
int64_t num_puzzle_pairs(int64_t N, int64_t K) {
    int n = (int)N, k = (int)K;
    if(k==0) {
        int64_t *f = calcF(n);
        int64_t cnt = 0;
        for(int i=1; i<= n; i++) { { if(f[i] > i && f[i] <= n && f[f[i]] == i) { cnt++; } } }
        free(f);
        { return cnt; }
    }
    int64_t res = 0;
    int64_t *f = calcF(n);
    int fmax = 0;
    for(int i=1; i<= n; i++) { { if((int)f[i] > fmax) { fmax = (int)f[i]; } } }
    int offset = 1;
    int maxQ = (n + k) + offset; 
    int maxP = fmax + offset;
    int Y_range = (maxP > maxQ) ? maxP : maxQ;
    P *pts = (P*)malloc(n * sizeof(P));
    if(!pts) { { exit(1); } }
    for(int i=1; i<= n; i++) { { pts[i-1].x = i; pts[i-1].y = (int)f[i] + offset; } }
    Q *qs = (Q*)malloc(2*n * sizeof(Q));
    if(!qs) { { exit(1); } }
    int qcount = 0, orig = 0;
    for(int p=1; p<= n; p++) {
        { int A = (p - k < 0) ? 0 : p - k;
          int B = p + k;
          int L = ((p + 1) > ((int)f[p] - k)) ? p + 1 : (int)(f[p] - k);
          int R = (n < ((int)f[p] + k)) ? n : (int)(f[p] + k);
          if(L > R) { { continue; } }
          { qs[qcount].L = L; qs[qcount].R = R; qs[qcount].y = B + offset; qs[qcount].id = orig; qs[qcount].sg = 1; qcount++; }
          { qs[qcount].L = L; qs[qcount].R = R; qs[qcount].y = (A - 1) + offset; qs[qcount].id = orig; qs[qcount].sg = -1; qcount++; }
          { orig++; }
        }
    }
    countSortP(pts, n, Y_range);
    countSortQ(qs, qcount, Y_range);
    int *BIT = (int*)calloc(n+1, sizeof(int));
    if(!BIT) { { exit(1); } }
    int pi = 0;
    int *ans = (int*)calloc(orig, sizeof(int));
    if(!ans) { { exit(1); } }
    for(int i=0; i< qcount; i++) {
        { while(pi < n && pts[pi].y <= qs[i].y) { { bit_upd(BIT, n, pts[pi].x, 1); pi++; } }
          int cnt = bit_qry(BIT, qs[i].R) - bit_qry(BIT, qs[i].L - 1);
          ans[qs[i].id] += qs[i].sg * cnt;
        }
    }
    for(int i=0; i< orig; i++) { { res += ans[i]; } }
    free(f); free(pts); free(qs); free(BIT); free(ans);
    { return res; }
}
int main(){
    printf("%s\n", num_puzzle_pairs(4, 2));
    return 0;
}