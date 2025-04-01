# type: ignore
from dataclasses import dataclass

@dataclass
class Node:
    val: int
    l: "Node | None" = None
    r: "Node | None" = None


def add(node, val):
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




