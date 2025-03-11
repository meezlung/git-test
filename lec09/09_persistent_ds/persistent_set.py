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
        return Node(node.val, add(node.l, val), node.r)
    elif val > node.val:
        return Node(node.val, node.l, add(node.r, val))
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


class Set:
    def __init__(self, root=None):
        self.root = root
        super().__init__()


    def add(self, val):
        return Set(add(self.root, val))


    def __contains__(self, val):
        return contains(self.root, val)




