# type: ignore

from dataclasses import dataclass

@dataclass
class Node[T]:
    value: T
    next: "Node[T] | None" = None


class Stack[T]:
    def __init__(self):
        self.sz = 0
        self.head = None
        super().__init__()

    def push(self, value) -> None:
        self.sz += 1
        self.head = Node(value, self.head)

    def pop(self) -> T:
        if self.sz == 0:
            raise ValueError

        self.sz -= 1
        value = self.head.value
        self.head = self.head.next
        return value

    def __len__(self):
        return self.sz
