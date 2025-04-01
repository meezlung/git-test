# type: ignore
from dataclasses import dataclass

from random import getrandbits

@dataclass
class Node:
    val: int
    priority: int
    l: "Node | None" = None
    r: "Node | None" = None


def split(node, val):
    # node points to a treap
    # returns three things.
    # - a treap consisting of all values < val
    # - a node containing val (if any)
    # - a treap consisting of all values > val
    if node is None:
        return None, None, None

    if val == node.val:
        l, r = node.l, node.r
        node.l = node.r = None
        return l, node, r

    if val < node.val:
        l, mid, node.l = split(node.l, val)
        return l, mid, node
    else:
        assert val > node.val
        node.r, mid, r = split(node.r, val)
        return node, mid, r


def merge(l, r):
    # l and r are treaps
    # every value in l is less than every value in r
    # return a single treap containing all of their nodes
    if l is None:
        return r
    if r is None:
        return l

    if l.priority > r.priority:
        # l will be the root
        l.r = merge(l.r, r)
        return l
    else:
        r.l = merge(l, r.l)
        return r


def add(node, val):
    l, mid, r = split(node, val)
    assert mid is None
    mid = Node(val, priority=getrandbits(64))
    return merge(merge(l, mid), r)


def remove(node, val):
    l, mid, r = split(node, val)
    assert mid is not None
    # free mid here
    return merge(l, r)


def contains(node, val):
    if node is None:
        return False

    if val < node.val:
        return contains(node.l, val)
    elif val > node.val:
        return contains(node.r, val)
    else:
        assert val == node.val
        return True


class OrderedSet:
    def __init__(self):
        self.root: Node | None = None
        super().__init__()


    def add(self, val):
        if val not in self:
            self.root = add(self.root, val)


    def remove(self, val):
        if val in self:
            self.root = remove(self.root, val)


    def __contains__(self, val):
        return contains(self.root, val)
