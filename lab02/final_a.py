# type: ignore

from collections.abc import Sequence
from dataclasses import dataclass

@dataclass
class Node:
    val:int
    level:int
    h:int=0
    l:"Node|None"=None
    r:"Node|None"=None
    subtree_sum:int=0
    subtree_min:int=0
    subtree_max:int=0
    def reset_height_sum(self):
        self.h=max(height(self.l),height(self.r))+1
        self.subtree_sum = self.level+(self.l.subtree_sum if self.l else 0)+(self.r.subtree_sum if self.r else 0)
        self.subtree_min = self.subtree_max = self.val
        if self.l is not None:
            self.subtree_min = min(self.subtree_min, self.l.subtree_min)
            self.subtree_max = max(self.subtree_max, self.l.subtree_max)
        if self.r is not None:
            self.subtree_min = min(self.subtree_min, self.r.subtree_min)
            self.subtree_max = max(self.subtree_max, self.r.subtree_max)
def height(node:Node|None):
    return -1 if not node else node.h
def join(l:Node|None,node:Node,r:Node|None):
    node.l=l
    node.r=r
    node.reset_height_sum()
    return node
def add_node(node:Node|None,val:int,level:int):
    return rebalance(_add_node(node,val,level))
def _add_node(node:Node|None,val:int,level:int):
    if node is None:
        return Node(val,level)
    if (val<node.val):
        node.l=add_node(node.l,val,level)
    elif (val > node.val):
        node.r=add_node(node.r,val,level)
    return node
def left_rotation(node):
    a,b,c,d,e=(node.l,node,node.r,node.r.l,node.r.r)
    return join(join(a,b,d),c,e)
def right_rotation(node):
    a,b,c,d,e=(node.l.l,node.l,node.l.r,node,node.r)
    return join(a,b,join(c,d,e))
def rebalance(node):
    if node is not None:
        node.reset_height_sum()
        if height(node.l)>=height(node.r)+2:
            if height(node.l.l)<height(node.l.r):
                node.l=left_rotation(node.l)
            node=right_rotation(node)
        elif height(node.r)>=height(node.l)+2:
            if height(node.r.r)<height(node.r.l):
                node.r=right_rotation(node.r)
            node=left_rotation(node)
    return node
def remove_node(node,v):
    return rebalance(_remove_node(node,v))
def _remove_node(node:Node|None,v):
    if node is None:
        return None
    if v<node.val:
        node.l=remove_node(node.l,v)
    elif v>node.val:
        node.r=remove_node(node.r,v)
    else:
        if node.l is None:
            return node.r
        if node.r is None:
            return node.l
        node.val, node.level, node.l = remove_rightmost(node.l)
    return node
def remove_rightmost(node):
    val,level,node=remove_rightmost_(node)
    return val,level,rebalance(node)
def remove_rightmost_(node):
    if node.r is None:
        return node.val,node.level,node.l
    else:
        val,level, node.r = remove_rightmost(node.r)
        return val,level,node
class PokemonTeam:
    def __init__(self, initial_team: Sequence[tuple[int, int]]):
        self.root=None
        for val,level in initial_team:
            self.root=add_node(self.root,val,level)

    def add(self, i: int, l: int):
        self.root=add_node(self.root,i,l)
        
    def remove(self, i: int):
        self.root=remove_node(self.root,i)

    def sum(self, i: int, j: int) -> int:
        def range_sum(node:Node|None,i:int,j:int) -> int:
            if node is None:
                return 0
            if node.subtree_max<i or node.subtree_min>j:
                return 0
            if i <= node.subtree_min and node.subtree_max <= j:
                return node.subtree_sum
            return (node.level if i<=node.val<=j else 0) + range_sum(node.l,i,j)+ range_sum(node.r,i,j)
        return range_sum(self.root,i,j)