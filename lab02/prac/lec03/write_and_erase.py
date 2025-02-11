# type: ignore

from dataclasses import dataclass
from random import getrandbits
import sys


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
        r.l = merge(l, r.l)
        return r
    

def add(node: Node, val: int):
    l, mid, r = split(node, val)
    mid = Node(val, priority=getrandbits(64))
    return merge(merge(l, mid), r)


def remove(node: Node, val: int):
    l, mid, r = split(node, val)
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
    

def count(node: Node):
    if node is None:
        return 0
    return 1 + count(node.l) + count(node.r)


class OrderedSet:
    def __init__(self):
        self.root: Node | None = None

    def add(self, val: int):
        if val not in self:
            self.root = add(self.root, val)

    def remove(self, val: int):
        if val in self:
            self.root = remove(self.root, val)

    def __contains__(self, val: int):
        return contains(self.root, val)
    
    def count(self):
        return count(self.root)
    

ordered_set = OrderedSet()

N = int(sys.stdin.readline())

for i in range(N):
    data = int(sys.stdin.readline().strip())

    if data in ordered_set:
        ordered_set.remove(data)
    else:
        ordered_set.add(data)

print(ordered_set.count())