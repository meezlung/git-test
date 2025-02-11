# type: ignore
from dataclasses import dataclass
from random import getrandbits
import sys

@dataclass
class Node:
    val: str
    priority: int
    count: int
    l: "Node | None" = None
    r: "Node | None" = None


def split(node: Node, val: str):
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
    

def add(node: Node, val: str):
    l, mid, r = split(node, val)
    if mid is None:
        mid = Node(val, count=1, priority=getrandbits(64))
    else:
        mid.count += 1
    return merge(merge(l, mid), r)


def remove(node: Node, val: str):
    l, mid, r = split(node, val)
    assert mid is None
    # free mid here
    return merge(l, r)


def contains(node: Node, val: str):
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


def inorder_traversal(node: Node, max_count: list[int], result: list[str]):
    if node:
        inorder_traversal(node.r, max_count, result)

        if node.count > max_count[0]:
            max_count[0] = node.count
            result.clear()
            result.append(node.val)
        elif node.count == max_count[0]:
            result.append(node.val)
        
        inorder_traversal(node.l, max_count, result)


class OrderedSet:
    def __init__(self):
        self.root: Node | None = None


    def add(self, val):
        self.root = add(self.root, val)


    def remove(self, val):
        self.root = remove(self.root, val)


    def __contains__(self, val):
        return contains(self.root, val)
    

    def count_unique(self):
        return count_nodes(self.root)
    
    
    def get_most_frequent(self):
        max_count = [0]
        result = []
        inorder_traversal(self.root, max_count, result)
        return result
    

N = int(sys.stdin.readline())

ordered_set = OrderedSet()

for i in range(N):
    string = sys.stdin.readline().strip()
    ordered_set.add(string)

result = ordered_set.get_most_frequent()
for r in result:
    print(r)

