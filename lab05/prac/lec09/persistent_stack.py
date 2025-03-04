from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass
class Node(Generic[T]):
    value: T
    next: "Node[T] | None" = None


class Stack(Generic[T]):
    def __init__(self, size: int = 0, head: "Node[T] | None" = None):
        self.size = size
        self.head = head

    def push(self, value: T) -> "Stack[T]":
        return Stack(self.size + 1, Node[T](value, self.head))

    def pop(self) -> "tuple[T, Stack[T]]":
        if self.size == 0:
            raise ValueError
        assert self.head is not None
        return (self.head.value, Stack[T](self.size - 1, self.head.next))
    
    def __len__(self):
        return self.size