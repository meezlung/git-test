# type: ignore

from dataclasses import dataclass

@dataclass(frozen=True)
class Node:
    val: int
    h: int         # height of the node
    size: int      # number of nodes in the subtree rooted at this node
    l: "Node | None" = None
    r: "Node | None" = None

def height(node: Node | None) -> int:
    return -1 if node is None else node.h

def subtree_size(node: Node | None) -> int:
    return 0 if node is None else node.size

def mk_node(val: int, l: Node | None, r: Node | None) -> Node:
    new_h = max(height(l), height(r)) + 1
    new_size = 1 + subtree_size(l) + subtree_size(r)
    return Node(val, new_h, new_size, l, r)

def join(l: Node | None, x: Node, r: Node | None) -> Node:
    return mk_node(x.val, l, r)

def left_rotate(x: Node) -> Node:
    # x.r must not be None
    y = x.r
    assert y is not None, "Right child must exist for left rotation"
    new_left = mk_node(x.val, x.l, y.l)
    return mk_node(y.val, new_left, y.r)

def right_rotate(x: Node) -> Node:
    # x.l must not be None
    y = x.l
    assert y is not None, "Left child must exist for right rotation"
    new_right = mk_node(x.val, y.r, x.r)
    return mk_node(y.val, y.l, new_right)

def rebalance(x: Node | None) -> Node | None:
    if x is None:
        return None

    if height(x.l) >= height(x.r) + 2:
        # Left heavy
        if height(x.l.l) < height(x.l.r):
            new_left = left_rotate(x.l)
            return right_rotate(mk_node(x.val, new_left, x.r))
        else:
            return right_rotate(x)
    elif height(x.r) >= height(x.l) + 2:
        # Right heavy
        if height(x.r.r) < height(x.r.l):
            new_right = right_rotate(x.r)
            return left_rotate(mk_node(x.val, x.l, new_right))
        else:
            return left_rotate(x)
    else:
        # Tree is balanced; update height and size.
        return mk_node(x.val, x.l, x.r)

def add(node: Node | None, val: int) -> Node:
    if node is None:
        return mk_node(val, None, None)
    if val < node.val:
        new_left = add(node.l, val)
        return rebalance(mk_node(node.val, new_left, node.r))
    elif val > node.val:
        new_right = add(node.r, val)
        return rebalance(mk_node(node.val, node.l, new_right))
    else:
        # Value already present, no change.
        return node

def remove_leftmost(node: Node) -> (int, Node | None):
    if node.l is None:
        return node.val, node.r
    else:
        left_val, new_left = remove_leftmost(node.l)
        return left_val, rebalance(mk_node(node.val, new_left, node.r))

def remove(node: Node | None, val: int) -> Node | None:
    if node is None:
        return None
    if val < node.val:
        new_left = remove(node.l, val)
        return rebalance(mk_node(node.val, new_left, node.r))
    elif val > node.val:
        new_right = remove(node.r, val)
        return rebalance(mk_node(node.val, node.l, new_right))
    else:
        # Found the node to remove.
        if node.l is None:
            return node.r
        if node.r is None:
            return node.l
        succ_val, new_right = remove_leftmost(node.r)
        return rebalance(mk_node(succ_val, node.l, new_right))

def contains(node: Node | None, val: int) -> bool:
    if node is None:
        return False
    if val < node.val:
        return contains(node.l, val)
    elif val > node.val:
        return contains(node.r, val)
    else:
        return True

def kth(node: Node | None, k: int) -> int:
    """Return the k-th smallest element (0-indexed)."""
    if node is None:
        raise IndexError("Index out of range")
    left_size = subtree_size(node.l)
    if k < left_size:
        return kth(node.l, k)
    elif k == left_size:
        return node.val
    else:
        return kth(node.r, k - left_size - 1)

def index_of(node: Node | None, val: int) -> int:
    """Return the index (0-indexed) of val in the tree. Raises ValueError if not found."""
    if node is None:
        raise ValueError("Value not found in OrderedSet")
    if val < node.val:
        return index_of(node.l, val)
    elif val > node.val:
        return subtree_size(node.l) + 1 + index_of(node.r, val)
    else:
        return subtree_size(node.l)

def lower_bound(node: Node | None, val: int) -> int | None:
    """Return the smallest value >= val, or None if no such value exists."""
    if node is None:
        return None
    if node.val < val:
        return lower_bound(node.r, val)
    else:
        candidate = lower_bound(node.l, val)
        return candidate if candidate is not None else node.val

def upper_bound(node: Node | None, val: int) -> int | None:
    """Return the smallest value > val, or None if no such value exists."""
    if node is None:
        return None
    if node.val <= val:
        return upper_bound(node.r, val)
    else:
        candidate = upper_bound(node.l, val)
        return candidate if candidate is not None else node.val

def to_list(node: Node | None) -> list:
    if node is None:
        return []
    return to_list(node.l) + [node.val] + to_list(node.r)

def tree_min(node: Node | None) -> int:
    if node is None:
        raise ValueError("Empty tree")
    while node.l is not None:
        node = node.l
    return node.val

def tree_max(node: Node | None) -> int:
    if node is None:
        raise ValueError("Empty tree")
    while node.r is not None:
        node = node.r
    return node.val

class OrderedSet:
    def __init__(self, root: Node | None = None):
        self.root = root

    def add(self, val: int) -> "OrderedSet":
        return OrderedSet(add(self.root, val))

    def remove(self, val: int) -> "OrderedSet":
        return OrderedSet(remove(self.root, val))

    def __contains__(self, val: int) -> bool:
        return contains(self.root, val)

    def __len__(self) -> int:
        return subtree_size(self.root)

    def __getitem__(self, index: int) -> int:
        if index < 0 or index >= len(self):
            raise IndexError("Index out of range")
        return kth(self.root, index)

    def index(self, val: int) -> int:
        """Return the index (0-indexed) of val in the OrderedSet.
           Raises ValueError if the value is not found."""
        return index_of(self.root, val)

    def __iter__(self):
        """Iterate over the values in sorted order."""
        return iter(to_list(self.root))

    def min(self) -> int:
        """Return the smallest element."""
        return tree_min(self.root)

    def max(self) -> int:
        """Return the largest element."""
        return tree_max(self.root)

    def lower_bound(self, val: int) -> int | None:
        """Return the smallest element >= val, or None if not found."""
        return lower_bound(self.root, val)

    def upper_bound(self, val: int) -> int | None:
        """Return the smallest element > val, or None if not found."""
        return upper_bound(self.root, val)

    def to_list(self) -> list:
        """Return the elements in sorted order as a list."""
        return to_list(self.root)

# Example usage:
s0 = OrderedSet()
s1 = s0.add(10)          # New set with 10 added.
s2 = s1.add(5).add(15)    # New set with 5 and 15 added.
print(s2[0])             # Prints 5, the smallest element.
print(s2.index(15))      # Prints 2, the index of value 15.
print(list(s2))          # Prints [5, 10, 15].
print(s2.lower_bound(11))  # Prints 15, the smallest element >= 11.
print(s2.upper_bound(10))  # Prints 15, the smallest element > 10.
print(s2.min(), s2.max())  # Prints the min and max values.
