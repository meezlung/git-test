# type: ignore

import random


class TreapNode:
    def __init__(self, val):
        self.val = val
        self.prio = random.getrandbits(64)
        self.left = None
        self.right = None
        super().__init__()


def find(t, x):
    if t is None:
        return None
    if t.val == x:
        return t
    if x < t.val:
        return find(t.left, x)
    else:
        return find(t.right, x)


def split(t, x):
    # l will have x_i < x, r will have x_i \geq x
    if t is None:
        return None, None
    elif x < t.val:
        r = t
        l, rr = split(t.left, x)
        r.left = rr
        return l, r
    elif x > t.val:
        l = t
        ll, r = split(t.right, x)
        l.right = ll
        return l, r
    else:
        assert t.val == x
        l = t.left
        r = t
        r.left = None
        return l, r


def merge(l, r):
    # assume values in l less than all values in r
    if l is None:
        return r
    if r is None:
        return l
    assert l.val < r.val
    if l.prio < r.prio:
        r.left = merge(l, r.left)
        return r
    else:
        l.right = merge(l.right, r)
        return l


def insert(t, nt):
    l, r = split(t, nt.val)
    return merge(merge(l, nt), r)


# def insert(t, nt):
#   if t is not None and t.prio > nt.prio:
#       if nt.val < t.val:
#           t.left = insert(t.left, nt)
#       else:
#           t.right = insert(t.right, nt)
#       return t
#   else:
#       l, r = split(t, nt.val)
#       nt.left = l
#       nt.right = r
#       return nt


def remove(t, x):
    if t is None:
        raise KeyError
    if x == t.val:
        nt = merge(t.left, t.right)
        return nt
    elif x < t.val:
        t.left = remove(t.left, x)
        return t
    else:  # x > t.val
        t.right = remove(t.right, x)
        return t


def height(t):
    if t is None:
        return 0
    h_l = height(t.left)
    h_r = height(t.right)
    prio_l = -1 if t.left is None else t.left.prio
    prio_r = -1 if t.right is None else t.right.prio
    assert t.prio > max(prio_l, prio_r)
    return max(h_l, h_r) + 1


def inorder(t):
    if t is not None:
        inorder(t.left)
    if t is not None:
        print(t.val)
    if t is not None:
        inorder(t.right)


def listify(t):
    li = []
    def _inorder(t):
        if t is not None:
            _inorder(t.left)
        if t is not None:
            li.append(t.val)
        if t is not None:
            _inorder(t.right)
    _inorder(t)
    assert sorted(li) == li
    return li


li = random.sample(range(1, 10000), 1000)
treap_set = None
for e in li:
    n = TreapNode(e)
    treap_set = insert(treap_set, n)
# inorder(treap_set)
sli = listify(treap_set)
print(height(treap_set))
# assert find(treap_set, -1) is None
# treap_set = remove(treap_set, -1)
for e in li:
    assert find(treap_set, e)
    treap_set = remove(treap_set, e)
