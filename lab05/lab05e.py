from collections.abc import Sequence
from dataclasses import dataclass

@dataclass
class Node:
    value: str
    next: "Node | None" = None

class Stack:
    def __init__(self, size: int = 0, head: "Node | None" = None):
        self.size = size
        self.head = head

    def push(self, value: str):
        return Stack(self.size + 1, Node(value, self.head))
    
    def pop(self):
        if self.size == 0:
            return None
        assert self.head is not None
        return (self.head.value, Stack(self.size - 1, self.head.next))
    
    def peek(self):
        if self.size == 0:
            return None
        assert self.head is not None
        return self.head.value

    def __len__(self):
        return self.size

class MenuPlanning:
    def __init__(self, initial_menu: Sequence[str]):
        self.n = len(initial_menu)

        init_stack = Stack(0)

        for menu in initial_menu:
            new = init_stack.push(menu)
            init_stack = new
        
        self.months: list[Stack] = [init_stack]

        super().__init__()

    def use_without_last(self, m: int) -> None:
        # new version with popped last element
        new_month = self.months[m].pop()

        if new_month is None:
            self.months.append(Stack(0))
            return

        self.months.append(new_month[1])

    def use_with_new(self, m: int, item: str) -> None:
        # new version with pushed new element
        new_month = self.months[m].push(item)
        self.months.append(new_month)

    def last_menu_item(self, m: int) -> str | None:
        # return the last
        last = self.months[m].peek()
        if last is None:
            return None
        return last
