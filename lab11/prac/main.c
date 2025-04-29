// geom_utils.c
// C equivalents of all geometry functions from Python modules
// Integer-only implementations

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <assert.h>

// --- Basic types & helpers --------------------------------------------

typedef struct { int64_t x, y; } Point;

int64_t gcd_ll(int64_t a, int64_t b) {
    while (b) {
        int64_t t = b;
        b = a % b;
        a = t;
    }
    return a;
}

int same_point(const Point *p, const Point *q) {
    return p->x == q->x && p->y == q->y;
}

// --- Primitives --------------------------------------------------------

int64_t dot(const Point *a, const Point *b) {
    return a->x*b->x + a->y*b->y;
}

int64_t cross(const Point *a, const Point *b) {
    return a->x*b->y - a->y*b->x;
}

int64_t orient(const Point *a, const Point *b, const Point *c) {
    Point v = { b->x - a->x, b->y - a->y };
    Point w = { c->x - a->x, c->y - a->y };
    return cross(&v, &w);
}

int on_segment(const Point *a, const Point *b, const Point *p) {
    return orient(a,b,p)==0 && dot(&(Point){p->x-a->x, p->y-a->y}, &(Point){p->x-b->x, p->y-b->y}) <= 0;
}

int segments_intersect(const Point *a,const Point *b,const Point *c,const Point *d) {
    int64_t o1 = orient(a,b,c), o2 = orient(a,b,d);
    int64_t o3 = orient(c,d,a), o4 = orient(c,d,b);
    if (o1*o2 < 0 && o3*o4 < 0) return 1;
    if (on_segment(a,b,c) || on_segment(a,b,d) || on_segment(c,d,a) || on_segment(c,d,b))
        return 1;
    return 0;
}

int64_t dist2(const Point *a, const Point *b) {
    int64_t dx = a->x - b->x;
    int64_t dy = a->y - b->y;
    return dx*dx + dy*dy;
}

// --- Simple Polyline/Polygon Checks -----------------------------------

int is_simple_polyline(const Point *pts, int n) {
    if (n < 2) return 0;
    for (int i = 0; i+1 < n; i++)
        if (same_point(&pts[i], &pts[i+1])) return 0;
    for (int i = 1; i+1 < n; i++)
        if (orient(&pts[i-1], &pts[i], &pts[i+1]) == 0) return 0;
    for (int i = 0; i+1 < n; i++)
        for (int j = i+2; j+1 < n; j++)
            if (segments_intersect(&pts[i],&pts[i+1],&pts[j],&pts[j+1]))
                return 0;
    return 1;
}

int is_simple_polygon(const Point *poly, int n) {
    if (n < 3) return 0;
    for (int i = 0; i < n; i++)
        if (same_point(&poly[i], &poly[(i+1)%n])) return 0;
    for (int i = 0; i < n; i++)
        if (orient(&poly[(i-1+n)%n], &poly[i], &poly[(i+1)%n]) == 0) return 0;
    for (int i = 0; i < n; i++) {
        for (int j = i+1; j < n; j++) {
            if (j == (i+1)%n || i == (j+1)%n) continue;
            if (segments_intersect(&poly[i],&poly[(i+1)%n],&poly[j],&poly[(j+1)%n]))
                return 0;
        }
    }
    return 1;
}

// --- Polygon area (2x area) -------------------------------------------

int64_t polygon_area2(const Point *poly, int n) {
    assert(is_simple_polygon(poly,n));
    int64_t A2 = 0;
    for (int i = 0; i < n; i++) {
        A2 += cross(&poly[i], &poly[(i+1)%n]);
    }
    return A2 < 0 ? -A2 : A2;
}

// --- Point-in-Polygon: Crossing Number --------------------------------

int point_in_polygon_crossing(const Point *p, const Point *poly, int n) {
    assert(is_simple_polygon(poly,n));
    int inside = 0;
    for (int i = 0; i < n; i++) {
        const Point *a = &poly[i];
        const Point *b = &poly[(i+1)%n];
        if (on_segment(a,b,p)) return 1;
        if ((a->y > p->y) != (b->y > p->y)) {
            int64_t cp = cross(&(Point){b->x-a->x, b->y-a->y}, &(Point){p->x-a->x, p->y-a->y});
            if (cp * (b->y - a->y) > 0) inside = !inside;
        }
    }
    return inside;
}

// --- Point-in-Polygon: Winding Number ---------------------------------

int point_in_polygon_winding(const Point *p, const Point *poly, int n) {
    assert(is_simple_polygon(poly,n));
    int wn = 0;
    for (int i = 0; i < n; i++) {
        const Point *a = &poly[i];
        const Point *b = &poly[(i+1)%n];
        if (on_segment(a,b,p)) return 1;
        if (a->y <= p->y) {
            if (b->y > p->y && orient(a,b,p) > 0) wn++;
        } else {
            if (b->y <= p->y && orient(a,b,p) < 0) wn--;
        }
    }
    return wn != 0;
}

// --- Point-in-Convex-Polygon (CCW-based) ------------------------------

int point_in_convex_polygon(const Point *p, const Point *poly, int n) {
    assert(n>=3);
    if (orient(&poly[0], &poly[1], p) < 0) return 0;
    if (orient(&poly[0], &poly[n-1], p) > 0) return 0;
    int lo = 1, hi = n-1;
    while (lo + 1 < hi) {
        int mid = (lo + hi)/2;
        if (orient(&poly[0], &poly[mid], p) >= 0) lo = mid;
        else hi = mid;
    }
    return orient(&poly[lo], &poly[hi], p) >= 0;
}

// --- 1D Range Counting ------------------------------------------------

int lower_bound_int(const int *arr, int n, int x) {
    int lo=0, hi=n;
    while (lo<hi) { int mid=(lo+hi)/2; if (arr[mid]<x) lo=mid+1; else hi=mid; }
    return lo;
}
int upper_bound_int(const int *arr, int n, int x) {
    int lo=0, hi=n;
    while (lo<hi) { int mid=(lo+hi)/2; if (arr[mid]<=x) lo=mid+1; else hi=mid; }
    return lo;
}
int range_count_1d(const int *arr, int n, int l, int r) {
    return upper_bound_int(arr,n,r) - lower_bound_int(arr,n,l);
}

// --- Fenwick Tree (1D) ------------------------------------------------

typedef struct { int n; int *f; } Fenwick;
Fenwick *fenwick_create(int n) { Fenwick *fw = malloc(sizeof(Fenwick)); fw->n=n; fw->f = calloc(n+1,sizeof(int)); return fw; }
void fenwick_update(Fenwick *fw, int i, int v) { for(; i<=fw->n; i+=i&-i) fw->f[i]+=v; }
int fenwick_query(const Fenwick *fw, int i) { int s=0; for(; i>0; i-=i&-i) s+=fw->f[i]; return s; }
int fenwick_range(const Fenwick *fw,int l,int r){ return fenwick_query(fw,r)-fenwick_query(fw,l-1); }

// --- KD-Tree for Nearest Neighbor -------------------------------------

typedef struct KDNode { Point pt; struct KDNode *left, *right; int axis; } KDNode;

KDNode *kd_build(Point *pts, int n, int depth) {
    if (n<=0) return NULL;
    int axis = depth % 2;
    int mid = n/2;
    // simple nth_element via qsort for demo
    qsort(pts, n, sizeof(Point), axis==0
          ? (int(*)(const void*,const void*))[](const Point *a,const Point *b){ return a->x - b->x; }
          : (int(*)(const void*,const void*))[](const Point *a,const Point *b){ return a->y - b->y; });
    KDNode *node = malloc(sizeof(KDNode));
    node->pt = pts[mid]; node->axis = axis;
    node->left  = kd_build(pts, mid, depth+1);
    node->right = kd_build(pts+mid+1, n-mid-1, depth+1);
    return node;
}

void kd_nearest(KDNode *node, const Point *target, Point *best_p, int64_t *best_d) {
    if (!node) return;
    int64_t d = dist2(target, &node->pt);
    if (d < *best_d) { *best_d = d; *best_p = node->pt; }
    int diff = (node->axis==0 ? target->x - node->pt.x : target->y - node->pt.y);
    KDNode *first = diff<0 ? node->left : node->right;
    KDNode *second = diff<0 ? node->right : node->left;
    kd_nearest(first, target, best_p, best_d);
    if ((int64_t)diff*diff < *best_d) kd_nearest(second, target, best_p, best_d);
}

// ... Additional range query structures omitted for brevity ...

// Example main for testing
int main() {
    Point tri[3] = {{0,0},{5,0},{0,5}};
    Point q = {1,1};
    printf("Crossing: %d\n", point_in_polygon_crossing(&q,tri,3));
    printf("Winding: %d\n", point_in_polygon_winding(&q,tri,3));
    printf("Convex: %d\n", point_in_convex_polygon(&q,tri,3));
    return 0;
}
