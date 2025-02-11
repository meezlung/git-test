#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef int64_t data_t;
typedef int64_t prio_t;

typedef struct Node {
    data_t val;
    prio_t priority;
    struct Node *l, *r;
} Node;


prio_t rand_prio() {
    prio_t res = 0;
    for (int i = 0; i < 4; i++) {
        res = (res << 16) ^ rand();
    }
    return res;
}


Node *create_node(data_t val) {
    Node *node = malloc(sizeof(Node));
    node->val = val;
    node->priority = rand_prio();
    node->l = node->r = NULL;
    return node;
}


void split(Node *node, data_t val, Node **l, Node **mid, Node **r) {
    if (node == NULL) {
        *l = *mid = *r = NULL;
    } else if (val == node->val) {
        *l = (node->l);
        *mid = node;
        *r = (node->r);
        node->l = node->r = NULL;
    } else if (val < node->val) {
        *r = node;
        split(node->l, val, l, mid, &(node->l));
    } else {
        assert(val > node->val);
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


Node *add(Node *node, data_t val) {
    Node *l, *mid, *r = malloc(sizeof(Node));
    split(node, val, l, mid, r);
    if (!mid) {
        mid = create_node(val);
    }
    return merge(merge(l, mid), r);
}


Node *remove(Node *node, data_t val) {
    Node *l, *mid, *r = malloc(sizeof(Node));
    split(node, val, l, mid, r);
    if (mid) {
        free(mid);
    }
    return merge(l, r);
}


bool contains(Node *node, data_t val) {
    if (!node) {
        return false;
    }

    if (val < node->val) {
        return contains(node->l, val);
    } else if (val > node->val) {
        return contains(node->r, val);
    } else {
        return true;
    }
}


int height(Node *node) {
    if (!node) {
        return 0;
    }
    data_t lh = height(node->l);
    data_t rh = height(node->r);
    return 1 + (lh > rh ? lh: rh);
}


int count_nodes(Node *node) {
    if (!node) {
        return 0;
    }
    return 1 + count_nodes(node->l) + count_nodes(node->r);
}



// class OrderedSet

typedef struct {
    Node *root;
    int size;
} OrderedSet;

void ordered_set_init(OrderedSet *set) {
    set->root = NULL;
}

void ordered_set_add(OrderedSet *set, data_t val) {
    if (!contains(set->root, val)) {
        set->root = add(set->root, val);
        set->size++;
    }
}

void ordered_set_remove(OrderedSet *set, data_t val) {
    if (contains(set->root, val)) {
        set->root = remove(set->root, val);
        set->size--;
    }
}

int ordered_set_count(OrderedSet *set) {
    return count_nodes(set->root);
}

void free_tree(Node *node) {
    if (!node) {
        return;
    }
    free_tree(node->l);
    free_tree(node->r);
    free(node);
}

void ordered_set_free(OrderedSet *set) {
    free_tree(set->root);
    set->root = NULL;
}

int main() {
    int N;
    scanf("%d", &N);

    OrderedSet *set = malloc(sizeof(OrderedSet));
    ordered_set_init(set);

    
    ordered_set_free(set);
    free(set);
    
    return 0;
}



