#include <bits/stdc++.h>
using namespace std;

using data_t = int64_t;
using prio_t = mt19937::result_type;


// good RNG
unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
mt19937 rng(seed);

prio_t rand_prio() {
    return rng();
}


template <class T>
struct Node {
    T v;
    Node<T> *l, *r;
    prio_t p;

    Node(T v, Node<T> *l = nullptr, Node<T> *r = nullptr): v(v), l(l), r(r), p(rand_prio()) {}
};


template <class T>
void n_split(Node<T> *n, const T &v, Node<T> *&l, Node<T> *&x, Node<T> *&r) {
    if (n == nullptr) {
        l = x = r = nullptr;
    } else if (v < n->v) {
        r = n;
        n_split(n->l, v, l, x, n->l);
    } else if (v > n->v) {
        l = n;
        n_split(n->r, v, n->r, x, r);
    } else {
        assert(v == n->v);
        l = n->l;
        x = n;
        r = n->r;
        n->l = n->r = nullptr;
    }
}


template <class T>
Node<T> *n_merge(Node<T> *l, Node<T> *r) {
    if (l == nullptr) {
        return r;
    }
    if (r == nullptr) {
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


template <class T>
Node<T> *n_add(Node<T> *n, const T &v) {
    Node<T> *l, *x, *r;
    n_split(n, v, l, x, r);
    assert(x == nullptr);
    x = new Node(v);
    return n_merge(n_merge(l, x), r);
}


template <class T>
Node<T> *n_remove(Node<T> *n, const T &v) {
    assert(n != nullptr);
    Node<T> *l, *x, *r;
    n_split(n, v, l, x, r);
    assert(x != nullptr && v == x->v);
    delete x;
    return n_merge(l, r);
}


template <class T>
bool n_contains(Node<T> *n, const T &v) {
    if (n == nullptr) {
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


template <class T>
T n_next_larger(Node<T> *n, const T &v) {
    if (n == nullptr) {
        return v;
    }

    if (v < n->v) {
        T r = n_next_larger(n->l, v);
        assert(r >= v);
        return r > v ? r : n->v;
    } else {
        return n_next_larger(n->r, v);
    }
}


template <class T>
struct Set {
    Node<T> *root = nullptr;
    int _size = 0;


    bool contains(const T &v) const {
        return n_contains(root, v);
    }


    bool add(const T &v) {
        if (contains(v)) {
            return false;
        } else {
            root = n_add(root, v);
            _size++;
            assert(_size >= 0);
            return true;
        }
    }


    bool remove(const T &v) {
        if (!contains(v)) {
            return false;
        } else {
            root = n_remove(root, v);
            _size--;
            assert(_size >= 0);
            return true;
        }
    }


    T next_larger(const T &v) const {
        return n_next_larger(root, v);
    }


    int size() const {
        return _size;
    }
};


int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<Set<data_t>> sets;
    while (q--) {
        string typ;
        cin >> typ;
        if (typ == "make") {
            sets.emplace_back();
        } else if (typ == "add") {
            int idx; data_t v;
            cin >> idx >> v;
            assert(0 <= idx && idx < sets.size());
            cout << sets[idx].add(v) << '\n';
        } else if (typ == "remove") {
            int idx; data_t v;
            cin >> idx >> v;
            assert(0 <= idx && idx < sets.size());
            cout << sets[idx].remove(v) << '\n';
        } else if (typ == "contains") {
            int idx; data_t v;
            cin >> idx >> v;
            assert(0 <= idx && idx < sets.size());
            cout << sets[idx].contains(v) << '\n';
        } else if (typ == "next_larger") {
            int idx; data_t v;
            cin >> idx >> v;
            assert(0 <= idx && idx < sets.size());
            data_t r = sets[idx].next_larger(v);
            if (r > v) {
                cout << r << '\n';
            } else {
                assert(r == v);
                cout << "!\n";
            }
        } else if (typ == "len") {
            int idx;
            cin >> idx;
            assert(0 <= idx && idx < sets.size());
            cout << sets[idx].size() << '\n';
        } else {
            assert(false);
        }
    }
}
