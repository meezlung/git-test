#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "pokedex.h"

typedef const char* data_t;
typedef int64_t prio_t;


typedef struct Node {
    data_t val;
    prio_t priority;
    struct Node *l, *r;
} Node;

typedef struct Pokedex {
    Node *pd;
} Pokedex;

Node *create_node(data_t val);
void split(Node *node, data_t val, Node **l, Node **mid, Node **r);
Node *merge(Node *l, Node *r);
Node *n_add(Node *node, data_t val);
bool contains(Node *node, data_t val);
const char *find_beside(Node *node, data_t val, Direction dir, const char **best);


Node *create_node(data_t val) {
    Node *node = malloc(sizeof(Node));
    node->val = val;
    node->priority = oj_rand();
    node->l = node->r = NULL;
    return node;
}


void split(Node *node, data_t val, Node **l, Node **mid, Node **r) {
    if (node == NULL) {
        *l = *mid = *r = NULL;
        return;
    } 
    
    int cmp = strcmp(val, node->val);
    if (cmp == 0) {
        *l = (node->l);
        *mid = node;
        *r = (node->r);
        node->l = node->r = NULL;
    } else if (cmp < 0) {
        *r = node;
        split(node->l, val, l, mid, &(node->l));
    } else {
        assert(cmp > 0);
        *l = node;
        split(node->r, val, &(node->r), mid, r);
    }
}


Node *merge(Node *l, Node *r) {
    if (l == NULL) {
        return r;
    }
    if (r == NULL) {
        return l;
    }

    if (l->priority > r->priority) {
        // l becomes the root
        l->r = merge(l->r, r);
        return l;
    } else {
        // r becomes the root
        r->l = merge(l, r->l);
        return r;
    }
}


Node *n_add(Node *node, data_t val) {
    Node *l, *mid, *r;
    split(node, val, &l, &mid, &r);
    if (!mid) {
        mid = create_node(val);
    }
    return merge(merge(l, mid), r);
}


bool contains(Node *node, data_t val) {
    if (!node) {
        return false;
    }

    int cmp = strcmp(val, node->val);
    if (cmp < 0) {
        return contains(node->l, val);
    } else if (cmp > 0) {
        return contains(node->r, val);
    } else {
        return true;
    }
}


const char *find_beside(Node *node, data_t val, Direction dir, const char **best) {
    if (!node) {
        return NULL;
    }

    int cmp = strcmp(val, node->val);

    if (cmp == 0) {
        if (dir == BEFORE) {
            Node *current = node->l;
            while (current && current->r) {
                current = current->r;
            }
            return current ? current->val : *best;
        } else if (dir == AFTER) {
            Node *current = node->r;
            while (current && current->l) {
                current = current->l;
            }
            return current ? current->val : *best;
        }
    } else if (cmp < 0) {
        if (dir == AFTER) {
            *best = node->val;  
        }
        return find_beside(node->l, val, dir, best);
    } else {
        if (dir == BEFORE) {
            *best = node->val;  
        }
        return find_beside(node->r, val, dir, best);
    }
}


Pokedex *pd_make() {
    Pokedex *pd = malloc(sizeof(Pokedex));
    pd->pd = NULL;
    return pd;
}


void pd_catch(Pokedex *p, const char *name) {
    if (!p || !name) {
        return;
    }

    if (!contains(p->pd, name)) {
        p->pd = n_add(p->pd, name);
    }
}


const char *pd_beside(Pokedex *p,  Direction direction, const char *name) {
    if (!p || !p->pd || !name) {
        return NULL;
    }
    
    const char *best = NULL;
    return find_beside(p->pd, name, direction, &best);
}