from dataclasses import dataclass, field
from collections.abc import Sequence

@dataclass
class Edge:
    child: str
    parent: str

@dataclass
class Node:
    label: str
    parent: "Node | None" = None
    depth: int = 0
    children: "list[Node]" = field(default_factory=list)
    jump: "list[Node]" = field(default_factory=list)


class RootedTree:
    def __init__(self, parent: Sequence[Edge], _root: str):
        n = len(parent)

        nodes: set[str] = set()
        for edge in parent:
            nodes.add(edge.child)
            nodes.add(edge.parent)
        self.node_idx: dict[str, int] = {node: idx for idx, node in enumerate(nodes)}

        self.edges: dict[str, str] = {edge.child: edge.parent for edge in parent} # child->parent

        self.root = root = self.node_idx[_root]

        





        
