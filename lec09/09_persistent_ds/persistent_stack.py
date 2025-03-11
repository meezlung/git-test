# type: ignore

from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class Node(Generic[T]):
    value: T
    next: "Node[T] | None" = None


class Stack[T]:
    def __init__(self, sz=0, head=None):
        self.sz = sz
        self.head = head
        super().__init__()

    def push(self, value) -> "Stack[T]":
        return Stack(self.sz + 1, Node(value, self.head))

    def pop(self) -> "tuple[T, Stack[T]]":
        if self.sz == 0:
            raise ValueError
        return (self.head.value, Stack(self.sz - 1, self.head.next))

    def __len__(self):
        return self.sz
