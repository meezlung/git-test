# type: ignore
from dataclasses import dataclass

@dataclass
class Node:
    val: int
    h: int = 0
    l: "Node | None" = None
    r: "Node | None" = None

    def reset_height(self):
        self.h = max(height(self.l), height(self.r)) + 1


def join(l, x, r):
    x.l = l
    x.r = r
    x.reset_height()
    return x


def height(node):
    return -1 if node is None else node.h


def left_rotate(x):
    (a, b, c, d, e) = (x.l, x, x.r.l, x.r, x.r.r)
    return join(join(a, b, c), d, e)


def right_rotate(x):
    (a, b, c, d, e) = (x.l.l, x.l, x.l.r, x, x.r)
    return join(a, b, join(c, d, e))


def rebalance(x):
    if x is not None:
        # reset height
        x.reset_height()
        if height(x.l) >= height(x.r) + 2:
            if height(x.l.l) < height(x.l.r):
                x.l = left_rotate(x.l)
            x = right_rotate(x)
        elif height(x.r) >= height(x.l) + 2:
            if height(x.r.r) < height(x.r.l):
                x.r = right_rotate(x.r)
            x = left_rotate(x)

    return x


def add(node, val):
    return rebalance(_add(node, val))


def _add(node, val):
    if node is None:
        return Node(val)

    if val < node.val:
        node.l = add(node.l, val)
    elif val > node.val:
        node.r = add(node.r, val)
    else:
        assert val == node.val

    return node


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


def remove(node, val):
    return rebalance(_remove(node, val))


def _remove(node, val):
    if node is None:
        return None

    if val < node.val:
        node.l = remove(node.l, val)
    elif val > node.val:
        node.r = remove(node.r, val)
    else:
        assert val == node.val
        if node.l is None:
            return node.r
        if node.r is None:
            return node.l
        node.val, node.r = remove_leftmost(node.r)

    return node


def remove_leftmost(node):
    val, node = _remove_leftmost(node)
    return val, rebalance(node)


def _remove_leftmost(node):
    assert node is not None
    if node.l is None:
        return node.val, node.r
    else:
        val, node.l = remove_leftmost(node.l)
        return val, node


class OrderedSet:
    def __init__(self):
        self.root: Node | None = None
        super().__init__()


    def add(self, val):
        self.root = add(self.root, val)


    def remove(self, val):
        self.root = remove(self.root, val)


    def __contains__(self, val):
        return contains(self.root, val)
