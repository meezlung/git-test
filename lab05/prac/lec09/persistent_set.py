from dataclasses import dataclass

@dataclass
class Node:
    val: int
    l: "Node | None" = None
    r: "Node | None" = None


def add(node: Node | None, val: int) -> Node:
    if node is None:
        return Node(val, None, None)
    
    if val < node.val:
        return Node(node.val, add(node.l, val), node.r)
    elif val > node.val:
        return Node(node.val, node.l, add(node.r, val))
    else:
        assert val == node.val
        
    return node


def remove(node: Node | None, val: int) -> Node | None:
    if node is None:
        return None
    
    if val < node.val:
        return Node(node.val, remove(node.l, val), node.r)
    elif val > node.val:
        return Node(node.val, node.l, remove(node.r, val))
    else:
        assert val == node.val
        
        # found the node to remove
        if node.l is not None:
            return node.r
        if node.r is not None:
            return node.l
        
        # node with two children
        assert node.r is not None
        successor_val = find_min(node.r) # find the in-order successor
        new_right = remove(node.r, successor_val)
        return Node(successor_val, node.l, new_right)


def find_min(node: Node) -> int:
    # Returns the smallest value in the subtree.
    while node.l is not None:
        node = node.l
    return node.val


def inorder(node: Node | None): # type: ignore
    if node is None:
        return
    yield from inorder(node.l)
    yield node.val
    yield from inorder(node.r)


def contains(node: Node | None, val: int) -> bool:
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
    def __init__(self, root: Node | None = None):
        self.root = root

    def add(self, val: int):
        return OrderedSet(add(self.root, val))
    
    def remove(self, val: int):
        return OrderedSet(remove(self.root, val))

    def __contains__(self, val: int):
        return contains(self.root, val)
    
    def __iter__(self): # type: ignore
        return inorder(self.root) # type: ignore
    
    


