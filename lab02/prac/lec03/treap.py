# type: ignore
from dataclasses import dataclass
from random import getrandbits

@dataclass
class Node:
    val: int
    priority: int
    l: "Node | None" = None
    r: "Node | None" = None


def split(node: Node, val: int):
    if node is None:
        return None, None, None
    
    if val == node.val:
        l, r = node.l, node.r
        node.l = node.r = None
        return l, node, r
    elif val < node.val:
        l, mid, node.l = split(node.l, val)
        return l, mid, node
    else:
        assert val > node.val
        node.r, mid, r = split(node.r, val)
        return node, mid, r
    

def merge(l: Node, r: Node):
    if l is None:
        return r
    if r is None:
        return l
    
    if l.priority > r.priority:
        # l will be the root
        l.r = merge(l.r, r)
        return l
    else:
        # r will be the root
        r.l = merge(l, r.l)
        return r
    

def add(node: Node, val: int):
    l, mid, r = split(node, val)
    assert mid is None
    mid = Node(val, priority=getrandbits(64))
    return merge(merge(l, mid), r)


def remove(node: Node, val: int):
    l, mid, r = split(node, val)
    assert mid is None
    # free mid here
    return merge(l, r)


def contains(node: Node, val: int):
    if node is None:
        return False
    
    if val < node.val:
        return contains(node.l, val)
    elif val > node.val:
        return contains(node.r, val)
    else:
        assert val == node.val
        return True


def height(node: Node):
    if node is None:
        return 0
    return 1 + max(height(node.l), height(node.r))


def count_nodes(node: Node):
    if node is None:
        return 0
    return 1 + count_nodes(node.l) + count_nodes(node.r)


class OrderedSet:
    def __init__(self):
        self.root: Node | None = None


    def add(self, val):
        if val not in self:
            self.root = add(self.root, val)


    def remove(self, val):
        if val in self:
            self.root = remove(self.root, val)


    def __contains__(self, val):
        return contains(self.root, val)
    

    def count(self):
        return count_nodes(self.root)
    