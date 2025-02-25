# type: ignore

from dataclasses import dataclass
from collections.abc import Sequence

@dataclass
class Node:
    val: int
    level: int
    height: int = 1
    subtree_sum: int = 0  
    l: "Node | None" = None
    r: "Node | None" = None

    def __post_init__(self):
        self.subtree_sum = self.level  

def get_height(node: Node | None) -> int:
    return node.height if node else 0

def get_balance(node: Node | None) -> int:
    return get_height(node.l) - get_height(node.r) if node else 0

def get_subtree_sum(node: Node | None) -> int:
    return node.subtree_sum if node else 0

def update_metadata(node: Node):
    node.height = max(get_height(node.l), get_height(node.r)) + 1
    node.subtree_sum = node.level + get_subtree_sum(node.l) + get_subtree_sum(node.r)

def rotate_right(y: Node) -> Node:
    x = y.l
    T2 = x.r if x else None

    x.r = y
    y.l = T2

    update_metadata(y)
    update_metadata(x)

    return x

def rotate_left(x: Node) -> Node:
    y = x.r
    T2 = y.l if y else None

    y.l = x
    x.r = T2

    update_metadata(x)
    update_metadata(y)

    return y

def balance(node: Node) -> Node:
    balance_factor = get_balance(node)
    if balance_factor > 1:
        if get_balance(node.l) < 0:
            node.l = rotate_left(node.l)  
        return rotate_right(node)

    if balance_factor < -1:
        if get_balance(node.r) > 0:
            node.r = rotate_right(node.r)  
        return rotate_left(node)

    update_metadata(node)
    return node

def add(node: Node | None, val: int, level: int) -> Node:
    if node is None:
        return Node(val, level)

    if val < node.val:
        node.l = add(node.l, val, level)
    elif val > node.val:
        node.r = add(node.r, val, level)
    else:
        return node  

    update_metadata(node)
    return balance(node)

def get_min_value_node(node: Node) -> Node:
    while node.l is not None:
        node = node.l
    return node

def remove(node: Node | None, val: int) -> Node | None:
    if node is None:
        return None

    if val < node.val:
        node.l = remove(node.l, val)
    elif val > node.val:
        node.r = remove(node.r, val)
    else:
        if node.l is None:
            return node.r
        elif node.r is None:
            return node.l
        
        temp = get_min_value_node(node.r)
        node.val, node.level = temp.val, temp.level
        node.r = remove(node.r, temp.val)

    update_metadata(node)
    return balance(node)


def range_sum(node: Node | None, i: int, j: int) -> int:
    stack: list[Node] = []
    current = node
    total_sum = 0

    while stack or current:
        if current:
            stack.append(current)
            if current.val < i:
                current = None
            else:
                current = current.l
        else:
            current = stack.pop()
            if i <= current.val <= j:
                total_sum += current.level
            if current.val <= j:
                current = current.r
            else:
                current = None

    return total_sum

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

class PokemonTeam:
    def __init__(self, initial_team: Sequence[tuple[int, int]]):
        self.root: Node | None = None
        
        for i, l in initial_team:
            if i not in self:
                self.root = add(self.root, i, l)

    def add(self, i: int, l: int):
        if i not in self:
            self.root = add(self.root, i, l)

    def remove(self, i: int):
        if i in self:
            self.root = remove(self.root, i)

    def sum(self, i: int, j: int) -> int:
        return range_sum(self.root, i, j)

    def __contains__(self, val: int) -> bool:
        return contains(self.root, val)