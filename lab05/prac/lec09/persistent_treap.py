# type: ignore

from dataclasses import dataclass
from random import getrandbits

@dataclass(frozen=True)
class Node:
    val: int
    priority: int
    l: "Node | None" = None
    r: "Node | None" = None

def split(node: Node | None, val: int):
    if node is None:
        return None, None, None
    
    if val == node.val:
        mid = Node(node.val, node.priority, None, None)
        return node.l, mid, node.r
    elif val < node.val:
        l, mid, new_left = split(node.l, val)
        new_node = Node(node.val, node.priority, new_left, node.r)
        return l, mid, new_node
    else:
        assert val > node.val
        new_right, mid, r = split(node.r, val)
        new_node = Node(node.val, node.priority, node.l, new_right)
        return new_node, mid, r


def merge(l: Node | None, r: Node | None):
    if l is None:
        return r
    if r is None:
        return l
    
    if l.priority > r.priority:
        # l.r = merge(l.r, r)
        # return l
        new_right = merge(l.r, r)
        return Node(l.val, l.priority, l.l, new_right)
    else:
        # r.l = merge(l, r.l)
        # return r
        new_left = merge(l, r.l)
        return Node(r.val, r.priority, new_left, r.r)


def add(node: Node, val: int):
    l, mid, r = split(node, val)
    assert mid is None
    mid = Node(val, priority=getrandbits(64))
    return merge(merge(l, mid), r)


def remove(node: Node, val: int):
    l, mid, r = split(node, val)
    assert mid is None
    # free
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
    return 1 + max(height(node.l), height(node,r))


def count_nodes(node: Node):
    if node is None:
        return 0
    return 1 + count_nodes(node.l) + count_nodes(node.r)


"""
Extra
"""

def kth(node: Node | None, k: int) -> int:
    """
    Returns the k-th smallest element (0-indexed) in the treap.
    """
    if node is None:
        raise IndexError("Index out of range")
    left_size = count_nodes(node.l)
    if k < left_size:
        return kth(node.l, k)
    elif k == left_size:
        return node.val
    else:
        return kth(node.r, k - left_size - 1)

def index_of(node: Node | None, val: int) -> int:
    """
    Returns the index (0-indexed) of val in the treap.
    Raises ValueError if not found.
    """
    if node is None:
        raise ValueError("Value not found in OrderedSet")
    if val < node.val:
        return index_of(node.l, val)
    elif val > node.val:
        return count_nodes(node.l) + 1 + index_of(node.r, val)
    else:
        return count_nodes(node.l)

def lower_bound(node: Node | None, val: int) -> int | None:
    """
    Returns the smallest value in the treap that is >= val,
    or None if no such value exists.
    """
    if node is None:
        return None
    if node.val < val:
        return lower_bound(node.r, val)
    else:
        candidate = lower_bound(node.l, val)
        return candidate if candidate is not None else node.val

def upper_bound(node: Node | None, val: int) -> int | None:
    """
    Returns the smallest value in the treap that is > val,
    or None if no such value exists.
    """
    if node is None:
        return None
    if node.val <= val:
        return upper_bound(node.r, val)
    else:
        candidate = upper_bound(node.l, val)
        return candidate if candidate is not None else node.val

def tree_min(node: Node | None) -> int:
    if node is None:
        raise ValueError("Empty treap")
    while node.l is not None:
        node = node.l
    return node.val

def tree_max(node: Node | None) -> int:
    if node is None:
        raise ValueError("Empty treap")
    while node.r is not None:
        node = node.r
    return node.val

def to_list(node: Node | None) -> list:
    if node is None:
        return []
    return to_list(node.l) + [node.val] + to_list(node.r)

class OrderedSet:
    def __init__(self, root: Node | None = None):
        self.root: Node | None = root

    def add(self, val: int):
        # if val not in self:
        #     self.root = add(self.root, val)
        if val in self:
            return val
        return OrderedSet(add(self.root, val))

    def remove(self, val: int):
        # if val in self:
        #     self.root = remove(self.root, val)
        if val not in self:
            return self
        return OrderedSet(remove(self.root, val))

    def __contains__(self, val: int):
        return contains(self.root, val)

    def count(self):
        return count_nodes(self.root)
    
    def __getitem__(self, i: int):
        if i < 0 or i >= len(self):
            raise IndexError("Index out of range")
        return kth(self.root, i)
    
    def __len__(self, i: int):
        return count_nodes(self.root)
    
    """
    Extra
    """

    def index(self, val: int) -> int:
        return index_of(self.root, val)

    def min(self) -> int:
        return tree_min(self.root)

    def max(self) -> int:
        return tree_max(self.root)

    def lower_bound(self, val: int) -> int | None:
        """
        Returns the smallest element >= val, or None if not found.
        """
        return lower_bound(self.root, val)

    def upper_bound(self, val: int) -> int | None:
        """
        Returns the smallest element > val, or None if not found.
        """
        return upper_bound(self.root, val)

    def to_list(self) -> list:
        return to_list(self.root)

    def __iter__(self):
        return iter(self.to_list())


if __name__ == "__main__":
    s0 = OrderedSet()
    s1 =  s0.add(10)          # New set with 10 added.
    s2 = s1.add(5).add(15)   # New set with 5 and 15 added.

    for s in s1:
        print(s)

    print()

    for s in s2:
        print(s)