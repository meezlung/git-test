#include <assert.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef int64_t data_t;
typedef int64_t prio_t;

#define PRIdata PRId64
#define SCNdata SCNd64

typedef struct Node {
    data_t v;
    struct Node *l, *r;
    prio_t p;
} Node;

typedef struct Set {
    Node *root;
    int size;
} Set;


prio_t rand_prio() {
    prio_t res = 0;
    for (int i = 0; i < 4; i++) {
        res = (res << 16) ^ rand();
    }
    return res;
}


void n_split(Node *n, data_t v, Node **l, Node **x, Node **r) {
    if (n == NULL) {
        *l = *x = *r = NULL;
    } else if (v < n->v) {
        *r = n;
        n_split(n->l, v, l, x, &(n->l));
    } else if (v > n->v) {
        *l = n;
        n_split(n->r, v, &(n->r), x, r);
    } else {
        assert(v == n->v);
        *l = n->l;
        *x = n;
        *r = n->r;
        n->l = n->r = NULL;
    }
}


Node *n_merge(Node *l, Node *r) {
    if (l == NULL) {
        return r;
    }
    if (r == NULL) {
        return l;
    }
    assert(l->v < r->v);
    if (l->p >= r->p) {
        l->r = n_merge(l->r, r);
        return l;
    } else {
        r->l = n_merge(l, r->l);
        return r;
    }
}


Node *n_make(data_t v, Node *l, Node *r) {
    Node *n = (Node*)malloc(sizeof(Node));
    n->v = v;
    n->l = l;
    n->r = r;
    n->p = rand_prio();
    return n;
}


Node *n_add(Node *n, data_t v) {
    Node *l, *x, *r;
    n_split(n, v, &l, &x, &r);
    assert(x == NULL);
    x = n_make(v, NULL, NULL);
    return n_merge(n_merge(l, x), r);
}


Node *n_remove(Node *n, data_t v) {
    assert(n != NULL);
    Node *l, *x, *r;
    n_split(n, v, &l, &x, &r);
    assert(x != NULL && v == x->v);
    free(x);
    return n_merge(l, r);
}


bool n_contains(Node *n, data_t v) {
    if (n == NULL) {
        return false;
    }

    if (v < n->v) {
        return n_contains(n->l, v);
    } else if (v > n->v) {
        return n_contains(n->r, v);
    } else {
        assert(v == n->v);
        return true;
    }
}


data_t n_next_larger(Node *n, data_t v) {
    if (n == NULL) {
        return v;
    }

    if (v < n->v) {
        data_t r = n_next_larger(n->l, v);
        assert(r >= v);
        return r > v ? r : n->v;
    } else {
        return n_next_larger(n->r, v);
    }
}


Set *s_make() {
    Set *s = (Set*)malloc(sizeof(Set));
    s->root = NULL;
    s->size = 0;
    return s;
}


bool s_contains(Set *s, data_t v) {
    return n_contains(s->root, v);
}


bool s_add(Set *s, data_t v) {
    if (s_contains(s, v)) {
        return false;
    } else {
        s->root = n_add(s->root, v);
        s->size++;
        assert(s->size >= 0);
        return true;
    }
}


bool s_remove(Set *s, data_t v) {
    if (!s_contains(s, v)) {
        return false;
    } else {
        s->root = n_remove(s->root, v);
        s->size--;
        assert(s->size >= 0);
        return true;
    }
}


data_t s_next_larger(Set *s, data_t v) {
    return n_next_larger(s->root, v);
}


int s_size(Set *s) {
    return s->size;
}


int main() {
    int q;
    scanf("%d", &q);
    char typ[111];
    Set **sets = (Set**)malloc(q * sizeof(Set*));
    int setc = 0;
    while (q--) {
        scanf("%s", typ);
        if (!strcmp(typ, "make")) {
            sets[setc++] = s_make();
        } else if (!strcmp(typ, "add")) {
            int idx; data_t v;
            scanf("%d%" SCNdata, &idx, &v);
            assert(0 <= idx && idx < setc);
            printf("%d\n", s_add(sets[idx], v));
        } else if (!strcmp(typ, "remove")) {
            int idx; data_t v;
            scanf("%d%" SCNdata, &idx, &v);
            assert(0 <= idx && idx < setc);
            printf("%d\n", s_remove(sets[idx], v));
        } else if (!strcmp(typ, "contains")) {
            int idx; data_t v;
            scanf("%d%" SCNdata, &idx, &v);
            assert(0 <= idx && idx < setc);
            printf("%d\n", s_contains(sets[idx], v));
        } else if (!strcmp(typ, "next_larger")) {
            int idx; data_t v;
            scanf("%d%" SCNdata, &idx, &v);
            assert(0 <= idx && idx < setc);
            data_t r = s_next_larger(sets[idx], v);
            if (r > v) {
                printf("%" PRIdata "\n", r);
            } else {
                assert(r == v);
                printf("!\n");
            }
        } else if (!strcmp(typ, "len")) {
            int idx;
            scanf("%d", &idx);
            assert(0 <= idx && idx < setc);
            printf("%d\n", s_size(sets[idx]));
        } else {
            assert(false);
        }
    }
}
